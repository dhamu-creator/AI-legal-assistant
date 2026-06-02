import mongoose from 'mongoose';
import dotenv from 'dotenv';

dotenv.config();

// Import models
import LegalDocument from './models/LegalDocument.js';
import EvidenceChecklist from './models/EvidenceChecklist.js';

const connectDB = async () => {
  try {
    const conn = await mongoose.connect(process.env.MONGO_URI);
    console.log(`✅ MongoDB Connected: ${conn.connection.host}`);
    return conn;
  } catch (error) {
    console.error(`❌ Error connecting to MongoDB: ${error.message}`);
    process.exit(1);
  }
};

const seedLegalDocuments = async () => {
  console.log('\n📚 Seeding Legal Documents...');

  const documents = [
    // IPC Sections - Theft
    {
      title: 'IPC Section 379 - Theft',
      type: 'IPC',
      content: 'Whoever, intending to take dishonestly any movable property out of the possession of any person without that person\'s consent, moves that property in order to such taking, is said to commit theft.',
      sectionNumber: '379',
      explanation: {
        en: 'Theft is taking something that belongs to someone else without permission with the intent to keep it.',
        ta: 'திருட்டு என்பது வேறு ஒருவருக்குச் சொந்தமான எதையும் அனுமதி இல்லாமல் எடுத்துக்கொள்ளுதல் ஆகும்.',
        hi: 'चोरी से मतलब किसी के सामान को बिना अनुमति के लेना है।',
        te: 'చోరీ అంటే ఎవరి వస్తువైనా అనుమతి లేకుండా తీసుకోవడం.',
        ml: 'മോഷണം എന്നത് മറ്റൊരാളുടെ സ്വത്ത് അനുമതി കൂടാതെ എടുക്കുന്നതാണ്.',
        ka: 'ಕಳ್ಳತನ ಎಂದರೆ ಬೇರೆ ಯಾರೊಬ್ಬರ ವಸ್ತುವನ್ನು ಅನುಮತಿ ಇಲ್ಲದೆ ತೆಗೆದುಕೊಳ್ಳುವುದು.'
      },
      punishment: 'Imprisonment up to 3 years and/or fine up to Rs. 250',
      rights: ['Right to legal representation', 'Right to bail', 'Right to fair trial'],
      relatedSections: ['380', '381', '382'],
      keyWords: ['theft', 'stolen', 'taking', 'dishonestly'],
      source: 'Indian Penal Code',
      year: 1860
    },

    // IPC Sections - Robbery
    {
      title: 'IPC Section 390 - Robbery',
      type: 'IPC',
      content: 'When five or more persons commit theft, it is called robbery.',
      sectionNumber: '390',
      explanation: {
        en: 'Robbery is theft committed by 5 or more people together, or with threat of violence.',
        ta: 'ஐந்து அல்லது அதற்கு மேற்பட்ட நபர்கள் திருட்டு செய்வது கொள்ளை ஆகும்.',
        hi: 'पाँच या अधिक लोग जब चोरी करते हैं तो इसे डकैती कहते हैं।',
        te: 'ఐదు లేదా అంతకంటే ఎక్కువ మందితో చేసిన చోరీ దానవ.',
        ml: 'അഞ്ച് അല്ലെങ്കിൽ അതിലധികം പേർ സംഘബദ്ധമായി കൊള്ളയടിക്കുന്നത് കൊള്ളയാണ്.',
        ka: 'ಐದು ಅಥವಾ ಹೆಚ್ಚಿನ ಜನರು ಒಟ್ಟಿಗೆ ಕಳ್ಳತನ ಮಾಡುವುದನ್ನು ಕಳ್ಳುಮಾರಿ ಎಂದು ಕರೆಯುತ್ತಾರೆ.'
      },
      punishment: 'Imprisonment up to 10 years and/or fine up to Rs. 1000',
      rights: ['Right to bail hearing', 'Right to fair investigation', 'Right to compensation'],
      relatedSections: ['391', '392', '393'],
      keyWords: ['robbery', 'dacoity', 'gang', 'violent'],
      source: 'Indian Penal Code',
      year: 1860
    },

    // BNS Sections - Cyber Crime
    {
      title: 'Information Technology Act 2000 - Section 66 (Cyber Fraud)',
      type: 'BNS',
      content: 'A person who commits computer fraud through unauthorized access or exceeding authorized access shall be punished with imprisonment.',
      sectionNumber: '66',
      explanation: {
        en: 'Cyber fraud includes hacking, unauthorized access to computer systems, phishing, and online scams.',
        ta: 'கணினி欺வு என்பது அননுமதிமான அணுக்கம், சொடுக்குவாரிகள் மற்றும் ஆன்லைன் மோசடி ஆகியவற்றை உள்ளடக்குகிறது.',
        hi: 'साइबर धोखाधड़ी में हैकिंग, अनधिकृत पहुंच और ऑनलाइन घोटाले शामिल हैं।',
        te: 'సైబర్ నష్టం హ్యాకింగ్, అননుమతిసంబంధమైన యాక్సెస్ మరియు ఆన్‌లైన్ స్కామ్‌లను కలిగి ఉంటుంది.',
        ml: 'സൈബർ വഞ്ചന ഹ്যാക്കിംഗ്, അননുമതിനിരത അ ക്സസ് എന്നിവ ഉൾക്കൊള്ളുന്നു.',
        ka: 'ಸೈಬರ್ ಹೋಲಿ ಜಾಲ ಹ್ಯಾಕಿಂಗ್, ಅನಧಿಕೃತ ಪ್ರವೇಶ ಮತ್ತು ಆನ್‌ಲೈನ್ ವಂಚನೆಗಳನ್ನು ಒಳಗೊಂಡಿದೆ.'
      },
      punishment: 'Imprisonment up to 3 years and/or fine up to Rs. 100,000',
      rights: ['Right to digital evidence protection', 'Right to anonymity if needed', 'Right to fair trial'],
      relatedSections: ['65', '67', '68', '69'],
      keyWords: ['cyber', 'hacking', 'fraud', 'online', 'phishing'],
      source: 'Information Technology Act 2000',
      year: 2000
    },

    // Domestic Violence
    {
      title: 'Protection of Women from Domestic Violence Act 2005',
      type: 'BSA',
      content: 'Protection against domestic violence. Any adult person who is in an intimate relationship with the respondent.',
      sectionNumber: '3',
      explanation: {
        en: 'This act protects women from physical, emotional, economic, or sexual abuse by family members or intimate partners.',
        ta: 'இந்த சட்டம் குடும்ப உறுப்பினர்கள் அல்லது நெருங்கிய உறவாளிகளால் ஏற்படும் உடல்ரீதி, உணர்வு, பொருளாதார அல்லது பாலியல் துன்பத்திலிருந்து பெண்களைப் பாதுகாக்கிறது.',
        hi: 'यह अधिनियम पारिवारिक सदस्यों या घनिष्ठ भागीदारों द्वारा किए जाने वाले शारीरिक, भावनात्मक, आर्थिक या यौन दुर्व्यवहार से महिलाओं की सुरक्षा करता है।',
        te: 'ఈ చట్టం కుటుంబ సభ్యులు లేదా సన్నిహిత భాగస్వాములచే చేయబడిన శారీరక, భావోద్వేగ, ఆర్థిక లేదా లైంగిక దుర్వ్యవహారం నుండి మహిళలను రక్షిస్తుంది.',
        ml: 'ഈ നിയമം കുടുംബ അംഗങ്ങൾ അല്ലെങ്കിൽ അടുത്ത സ്ഥിതിയിലുള്ള പങ്കാളികൾ നടത്തുന്ന ശാരീരിക, വൈകാരിക, സാമ്പത്തിക അല്ലെങ്കിൽ ലൈംഗിക ദുരുപയോഗത്തിൽ നിന്ന് സ്ത്രീകളെ സംരക്ഷിക്കുന്നു.',
        ka: 'ಈ ಅಧಿನಿಯಮವು ಕುಟುಂಬ ಸದಸ್ಯರು ಅಥವಾ ನೆರವೆಯ ಸಮೋಹಿತರಿಂದ ನಿರ್ವಹಿಸುವ ದೈಹಿಕ, ಭಾವನಾತ್ಮಕ, ಆರ್ಥಿಕ ಅಥವಾ ಲೈಂಗಿಕ ಸುಸಂಗತಿಯಿಂದ ಮಹಿಳೆಯರನ್ನು ರಕ್ಷಿಸುತ್ತದೆ.'
      },
      punishment: 'Protection order, maintenance, custody of children',
      rights: ['Right to protection order', 'Right to maintenance', 'Right to residence', 'Right to custody of children'],
      relatedSections: ['2', '4', '5', '6'],
      keyWords: ['domestic violence', 'abuse', 'family', 'women'],
      source: 'Protection of Women from Domestic Violence Act 2005',
      year: 2005
    },

    // Cyber Law - Online Harassment
    {
      title: 'Information Technology Act 2000 - Section 67 (Obscene Content)',
      type: 'BNS',
      content: 'Publishing or transmitting obscene material through computer networks.',
      sectionNumber: '67',
      explanation: {
        en: 'Covers online harassment, sending indecent pictures, and spreading abusive content online.',
        ta: 'ஆன்லைன் 騷நரைப்பு, அশ்லீல படங்களை அனுப்புதல் மற்றும் ஆன்லைனில் அவमानকരமான உள்ளடக்கத்தை பரவ்வுவதை உள்ளடக்குகிறது.',
        hi: 'ऑनलाइन उत्पीड़न, अश्लील तस्वीरें भेजना और अपमानजनक सामग्री फैलाना शामिल है।',
        te: 'ఆన్‌లైన్騚騚ఓ, అశ్లీల చిత్రాలను పంపడం మరియు ఆన్‌లైన్‌లో దుర్భాషలు ఉన్నత సామग్రీని కవర్ చేస్తుంది.',
        ml: 'ഓൺലൈൻ ഉപദ്രവം, അശ്ലീല ചിത്രങ്ങൾ അയയ്ക്കൽ, കൂടാതെ അഫോർമേറ്ററ് സാമഗ്രി ഓണ്‍ലൈന് പ്രചരിപ്പിക്കലും അതിൽ സാധ്യം.',
        ka: 'ಆನ್‌ಲೈನ್ ಕಿತ್ತೋಳಿಕೆ, ಅಶ್ಲೀಲ ಚಿತ್ರಗಳನ್ನು ಕಳುಹಿಸುವುದು ಮತ್ತು ಅಪಮಾನಕರ ವಿಷಯವಸ್ತುವನ್ನು ಆನ್‌ಲೈನ್‌ನಲ್ಲಿ ಪ್ರಸಾರಿಸುವುದನ್ನು ಒಳಗೊಂಡಿದೆ.'
      },
      punishment: 'Imprisonment up to 3 years and/or fine up to Rs. 100,000',
      rights: ['Right to privacy', 'Right to digital safety', 'Right to complaint'],
      relatedSections: ['66', '68', '69'],
      keyWords: ['harassment', 'obscene', 'online abuse', 'indecent'],
      source: 'Information Technology Act 2000',
      year: 2000
    }
  ];

  try {
    const result = await LegalDocument.insertMany(documents);
    console.log(`✅ Inserted ${result.length} legal documents`);
  } catch (error) {
    if (error.code === 11000) {
      console.log('⚠️  Some documents already exist (duplicate keys)');
    } else {
      console.error('❌ Error seeding legal documents:', error.message);
    }
  }
};

const seedEvidenceChecklists = async () => {
  console.log('\n📋 Seeding Evidence Checklists...');

  const checklists = [
    {
      crimeCategory: 'Theft',
      items: [
        {
          name: 'Original Receipt/Bill',
          description: 'Original purchase receipt showing date, price, and item details',
          importance: 'critical'
        },
        {
          name: 'Photographs of Item',
          description: 'Clear photos of the stolen item from multiple angles',
          importance: 'critical'
        },
        {
          name: 'Description of Item',
          description: 'Detailed description including color, size, brand, and distinctive features',
          importance: 'important'
        },
        {
          name: 'IMEI Number (if mobile)',
          description: 'IMEI number, SIM card details, and phone model number',
          importance: 'critical'
        },
        {
          name: 'Witness Statements',
          description: 'Names and statements of people who saw the theft',
          importance: 'important'
        }
      ],
      procedureSteps: [
        'Report theft to nearest police station immediately',
        'Get FIR copy and FIR number for insurance',
        'If mobile/laptop: Block SIM and freeze accounts',
        'Report to insurance company within 48 hours',
        'Keep communication copies with police for record'
      ],
      emergencyContacts: [
        {
          name: 'Police (Emergency)',
          number: '100',
          description: 'Call for immediate police assistance'
        },
        {
          name: 'Local Police Station',
          number: '1099',
          description: 'Register FIR for theft case'
        }
      ]
    },

    {
      crimeCategory: 'CyberFraud',
      items: [
        {
          name: 'Transaction Screenshots',
          description: 'Screenshots of unauthorized transactions and payment confirmations',
          importance: 'critical'
        },
        {
          name: 'Email Communications',
          description: 'All emails from the fraudster with headers',
          importance: 'critical'
        },
        {
          name: 'Bank Statements',
          description: 'Bank account statements showing fraudulent transactions',
          importance: 'critical'
        },
        {
          name: 'Website/App Screenshots',
          description: 'Screenshots of the fraudulent website or app used for scam',
          importance: 'important'
        },
        {
          name: 'Phone Call Records',
          description: 'Call logs and SMS from fraudster if available',
          importance: 'important'
        }
      ],
      procedureSteps: [
        'Stop any further communication with fraudster',
        'Take screenshots of all evidence immediately',
        'Report to bank and block cards/accounts',
        'File complaint with Cyber Police (1930)',
        'Report to cybercrime portal of your state',
        'Keep all documentation safely'
      ],
      emergencyContacts: [
        {
          name: 'Cyber Crime Portal',
          number: '1930',
          description: 'National Cybercrime Helpline'
        },
        {
          name: 'Local Police',
          number: '100',
          description: 'File FIR for cyber crime'
        },
        {
          name: 'Bank Fraud Department',
          number: 'Check your bank card',
          description: 'Contact your bank immediately'
        }
      ]
    },

    {
      crimeCategory: 'Harassment',
      items: [
        {
          name: 'Written Threats/Messages',
          description: 'Messages, emails, SMS, WhatsApp conversations showing harassment',
          importance: 'critical'
        },
        {
          name: 'Call Records',
          description: 'Call logs showing repeated calls, missed calls, or threatening calls',
          importance: 'critical'
        },
        {
          name: 'Witness Accounts',
          description: 'Names of people who witnessed the harassment',
          importance: 'important'
        },
        {
          name: 'Photos of Physical Evidence',
          description: 'If applicable - photos of defaced property or threatening material',
          importance: 'important'
        },
        {
          name: 'Timeline Document',
          description: 'Document with dates, times, and details of each harassment incident',
          importance: 'critical'
        }
      ],
      procedureSteps: [
        'Save all evidence (screenshots, call logs, messages)',
        'Do not respond or engage with harasser',
        'Document every incident with date and time',
        'Report to police station immediately',
        'File complaint under IPC 494, 504, 506 or 509',
        'Consider restraining order if needed'
      ],
      emergencyContacts: [
        {
          name: 'Women Helpline',
          number: '1091',
          description: 'For harassment/abuse against women'
        },
        {
          name: 'Police Emergency',
          number: '100',
          description: 'File FIR for harassment'
        }
      ]
    },

    {
      crimeCategory: 'DomesticViolence',
      items: [
        {
          name: 'Medical Reports',
          description: 'Medical examination reports documenting injuries',
          importance: 'critical'
        },
        {
          name: 'Photographs of Injuries',
          description: 'Dated photographs of bruises, injuries, and damage',
          importance: 'critical'
        },
        {
          name: 'Witness Statements',
          description: 'Statements from neighbors, family, or friends who witnessed abuse',
          importance: 'critical'
        },
        {
          name: 'Written Records',
          description: 'Diary entries, letters, or written accounts of incidents',
          importance: 'important'
        },
        {
          name: 'Phone Records/Messages',
          description: 'SMS, emails, or call logs showing threats or abuse',
          importance: 'important'
        }
      ],
      procedureSteps: [
        'Seek immediate medical attention for injuries',
        'File complaint at police station (FIR)',
        'Contact women shelter for immediate safety',
        'Get copy of medical report',
        'Apply for protection order from court',
        'Gather all evidence safely'
      ],
      emergencyContacts: [
        {
          name: 'Women Helpline',
          number: '1091',
          description: 'National Women Helpline - 24/7 available'
        },
        {
          name: 'Police Emergency',
          number: '100',
          description: 'File FIR for domestic violence'
        },
        {
          name: 'AAWHAN - Women Support',
          number: '9999 666 555',
          description: 'Support and counseling for women'
        }
      ]
    },

    {
      crimeCategory: 'IdentityTheft',
      items: [
        {
          name: 'Original Identity Documents',
          description: 'Aadhaar, PAN, Passport copies',
          importance: 'critical'
        },
        {
          name: 'Unauthorized Account Creation',
          description: 'Proof of accounts opened fraudulently in your name',
          importance: 'critical'
        },
        {
          name: 'Credit Reports',
          description: 'Credit report showing unauthorized transactions',
          importance: 'critical'
        },
        {
          name: 'Bank Statements',
          description: 'Statements showing fraudulent transactions',
          importance: 'critical'
        },
        {
          name: 'Communication Records',
          description: 'Any communication related to fraud',
          importance: 'important'
        }
      ],
      procedureSteps: [
        'File complaint with local police',
        'Contact all banks and credit agencies',
        'Freeze credit in all bureaus',
        'Report to cybercrime portal',
        'Change all passwords immediately',
        'Monitor accounts regularly for next 12 months'
      ],
      emergencyContacts: [
        {
          name: 'Cyber Crime Helpline',
          number: '1930',
          description: 'Report cyber/identity theft'
        },
        {
          name: 'CIBIL (Credit Bureau)',
          number: '1800-222-1111',
          description: 'Freeze credit profile'
        },
        {
          name: 'Police',
          number: '100',
          description: 'File FIR for identity theft'
        }
      ]
    }
  ];

  try {
    const result = await EvidenceChecklist.insertMany(checklists);
    console.log(`✅ Inserted ${result.length} evidence checklists`);
  } catch (error) {
    if (error.code === 11000) {
      console.log('⚠️  Some checklists already exist (duplicate keys)');
    } else {
      console.error('❌ Error seeding evidence checklists:', error.message);
    }
  }
};

const seedDatabase = async () => {
  try {
    await connectDB();

    console.log('\n🌱 Starting database seed...');
    await seedLegalDocuments();
    await seedEvidenceChecklists();

    console.log('\n✅ Database seeding completed successfully!');
    console.log('\n📊 Seeded Data:');
    console.log('   • 5 Legal Documents (IPC, BNS sections)');
    console.log('   • 5 Evidence Checklists (crime-specific)');

    return true;
  } catch (error) {
    console.error('❌ Seeding failed:', error.message);
    throw error;
  }
};

// Allow running as a script or importing as a module
const isMain = import.meta.url === `file://${process.argv[1]}`;
if (isMain) {
  seedDatabase()
    .then(() => process.exit(0))
    .catch(() => process.exit(1));
}

export default seedDatabase;
