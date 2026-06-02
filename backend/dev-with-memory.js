import { MongoMemoryServer } from 'mongodb-memory-server';
import { spawn } from 'child_process';

const wait = (ms) => new Promise((res) => setTimeout(res, ms));

const run = async () => {
  const mongod = await MongoMemoryServer.create();
  const uri = mongod.getUri();
  console.log('🟡 In-memory MongoDB URI:', uri);

  // Start backend server as child with MONGO_URI env
  const env = { ...process.env, MONGO_URI: uri, NODE_ENV: 'development' };
  // Enable test mode to avoid external LLM calls during automated tests
  env.TEST_MODE = 'true';
  const child = spawn(process.execPath, ['server.js'], { cwd: process.cwd(), env, stdio: 'inherit' });

  // Wait for server to boot and respond
  const base = 'http://localhost:5000';
  let ready = false;
  // Wait until server health + DB ready
  for (let i = 0; i < 120; i++) {
    try {
      const res = await fetch(`${base}/api/ready`);
      if (res.ok) {
        const json = await res.json().catch(() => ({}));
        if (json.ready) {
          ready = true;
          break;
        }
      }
    } catch (e) {
      // not ready yet
    }
    await wait(1000);
  }

  if (!ready) {
    console.error('❌ Backend did not become ready in time');
    child.kill();
    await mongod.stop();
    process.exit(1);
  }

    console.log('✅ Backend is ready. Running API checks...');

  try {
    // Helper: fetch with retries
    const fetchJsonWithRetry = async (url, options = {}, attempts = 5) => {
      for (let i = 0; i < attempts; i++) {
        try {
          const res = await fetch(url, options);
          const body = await res.json().catch(() => null);
          return { res, body };
        } catch (e) {
          console.warn(`Fetch attempt ${i + 1} failed for ${url}:`, e.message);
          await wait(500);
        }
      }
      throw new Error('fetch failed');
    };

    // Health
    const { res: healthRes, body: health } = await fetchJsonWithRetry(`${base}/api/health`);
    console.log('Health status:', healthRes.status, 'body:', health);

    // Languages
    const { res: langsRes, body: langs } = await fetchJsonWithRetry(`${base}/api/legal/languages`);
    console.log('Languages status:', langsRes.status, 'body:', langs);

    // Crime categories
    const { res: crimesRes, body: crimes } = await fetchJsonWithRetry(`${base}/api/legal/crime-categories`);
    console.log('Crime categories status:', crimesRes.status, 'body:', crimes);

    // Register a test user and obtain userId (uses auth endpoints)
    const randomHex = () => Array.from({ length: 24 }, () => Math.floor(Math.random() * 16).toString(16)).join('');
    const randomEmail = () => `test+${Date.now()}@example.com`;
    const regBody = { name: 'Test User', email: randomEmail(), password: 'Password123!', language: 'en' };
    let userId = null;
    try {
      // Use retry helper for auth flows
      const { body: regJson } = await fetchJsonWithRetry(`${base}/api/auth/register`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(regBody) }, 5);
      console.log('Register body:', regJson);

      const { body: loginJson } = await fetchJsonWithRetry(`${base}/api/auth/login`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email: regBody.email, password: regBody.password }) }, 5);
      console.log('Login body:', loginJson);
      const token = loginJson?.data?.token;
      if (token) {
        const { body: meJson } = await fetchJsonWithRetry(`${base}/api/auth/me`, { headers: { Authorization: `Bearer ${token}` } }, 5);
        console.log('Me body:', meJson);
        userId = meJson?.data?._id || meJson?.data?.id || (regJson?.data?.user?.id);
      }
    } catch (e) {
      console.error('Auth flow failed:', e.message);
    }

    let sessionResp = null;
    try {
      const res = await fetch(`${base}/api/chat/session`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId: userId || randomHex(), language: 'en' }),
      });
      sessionResp = await res.json();
      console.log('Create session response status:', res.status);
      console.log('Create session response body:', sessionResp);
    } catch (e) {
      console.error('Create session failed:', e.message);
    }

    // Send a message
    let sendResp = null;
    try {
      const res = await fetch(`${base}/api/chat/message`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId: sessionResp?.data?._id, message: 'I was robbed near my house last night', language: 'en' }),
      });
      sendResp = await res.json();
      console.log('Send message status:', res.status);
      console.log('Send message body:', sendResp);
    } catch (e) {
      console.error('Send message failed:', e.message);
    }

    // Create FIR
    let firCreateResp = null;
    try {
      const res = await fetch(`${base}/api/fir/create/${userId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: 'Robbery Test', incidentDetails: 'Robbed at night', incidentDate: '2026-05-28', incidentLocation: 'Test Street', complainantDetails: { name: 'Test User', phone: '9999999999', address: 'Test Address' } }),
      });
      firCreateResp = await res.json();
      console.log('Create FIR status:', res.status);
      console.log('Create FIR body:', firCreateResp);
    } catch (e) {
      console.error('Create FIR failed:', e.message);
    }

    // If create returned missing fields (400), try again with full required payload including crimeCategory
    if (firCreateResp && firCreateResp.success === false) {
      try {
        const fullPayload = {
          title: 'Robbery Test - Full',
          incidentDetails: 'Robbed at night, purse taken',
          incidentDate: new Date().toISOString(),
          incidentLocation: 'Test Street',
          crimeCategory: 'Robbery',
          complainantDetails: { name: 'Test User', phone: '9999999999', address: 'Test Address' },
          suspectDetails: { name: 'Unknown', description: 'Masked, medium build' },
          evidence: ['photo1.jpg'],
        };
        const res2 = await fetch(`${base}/api/fir/create/${userId}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(fullPayload),
        });
        const firCreateResp2 = await res2.json().catch(() => null);
        console.log('Retry Create FIR status:', res2.status);
        console.log('Retry Create FIR body:', firCreateResp2);
      } catch (e) {
        console.error('Retry Create FIR failed:', e.message);
      }
    }

    // Generate FIR draft via AI
    try {
      const incidentPayload = {
        incidentData: {
          complainantDetails: { name: 'Test User', phone: '9999999999', address: 'Test Address' },
          incidentDetails: 'Stolen mobile in market, pickpocket',
          incidentDate: new Date().toISOString(),
          incidentLocation: 'Test Market',
          suspectDetails: { name: 'Unknown', description: 'Masked person' },
          evidence: ['photo1.jpg'],
        },
        language: 'en',
      };
      const res = await fetch(`${base}/api/fir/generate/${userId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(incidentPayload),
      });
      const genResp = await res.json().catch(() => null);
      console.log('Generate FIR status:', res.status);
      console.log('Generate FIR body:', genResp);
    } catch (e) {
      console.error('Generate FIR failed:', e.message);
    }

    // Evidence checklist
    try {
      const res = await fetch(`${base}/api/fir/evidence/checklist`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ crimeCategory: 'Robbery', language: 'en' }),
      });
      const checklistResp = await res.json();
      console.log('Evidence checklist status:', res.status);
      console.log('Evidence checklist body:', checklistResp);
    } catch (e) {
      console.error('Evidence checklist failed:', e.message);
    }

  } catch (err) {
    console.error('❌ API checks failed:', err.message);
  }

  // Cleanup
  child.kill();
  await mongod.stop();
  console.log('🟡 Stopped backend and in-memory MongoDB');
};

run().catch((e) => {
  console.error('Fatal error:', e);
  process.exit(1);
});
