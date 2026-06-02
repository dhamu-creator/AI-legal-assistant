import { MongoMemoryServer } from 'mongodb-memory-server';
import seedDatabase from './seed.js';

// Start in-memory MongoDB, run seed, then stop
const run = async () => {
  const mongod = await MongoMemoryServer.create();
  const uri = mongod.getUri();
  console.log('🟡 Started in-memory MongoDB at', uri);

  // Set env for seed
  process.env.MONGO_URI = uri;

  try {
    await seedDatabase();
    console.log('🟢 Seeding completed against in-memory MongoDB');
  } catch (err) {
    console.error('❌ Seeding failed:', err.message);
    process.exitCode = 1;
  } finally {
    await mongod.stop();
    console.log('🟡 In-memory MongoDB stopped');
  }
};

run();
