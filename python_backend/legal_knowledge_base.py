# AI Legal Assistant - Legal Knowledge Base Module
# This module provides comprehensive legal information for Indian law
# Covers: BNS 2023, BNSS 2023, BSA 2023, IPC 1860, CrPC 1973,
#          IT Act 2000, PWDVA 2005, POCSO 2012, NDPS 1985, SC/ST Act 1989,
#          Motor Vehicles Act 1988

# ── Legal Acts & Sections Database ──────────────────────────────────────────

LEGAL_ACTS = {
    "BNS": {
        "name": "Bharatiya Nyaya Sanhita",
        "year": 2023,
        "description": "The new criminal law replacing IPC, applicable from July 2024",
        "fullForm": "Bharatiya Nyaya Sanhita, 2023",
        "chapters": 52
    },
    "BNSS": {
        "name": "Bharatiya Nagarik Suraksha Sanhita",
        "year": 2023,
        "description": "The new criminal procedure law replacing CrPC, applicable from July 2024",
        "fullForm": "Bharatiya Nagarik Suraksha Sanhita, 2023",
        "chapters": 18
    },
    "BSA": {
        "name": "Bharatiya Sakshya Adhiniyam",
        "year": 2023,
        "description": "The new Indian Evidence Act replacement",
        "fullForm": "Bharatiya Sakshya Adhiniyam, 2023",
        "chapters": 11
    },
    "IPC": {
        "name": "Indian Penal Code",
        "year": 1860,
        "description": "Original criminal code (being replaced by BNS)",
        "fullForm": "Indian Penal Code, 1860",
        "chapters": 45
    },
    "CrPC": {
        "name": "Criminal Procedure Code",
        "year": 1973,
        "description": "Original criminal procedure code (being replaced by BNSS)",
        "fullForm": "Code of Criminal Procedure, 1973",
        "chapters": 39
    },
    "IT_ACT": {
        "name": "Information Technology Act",
        "year": 2000,
        "description": "Law governing cybercrime and digital evidence",
        "fullForm": "Information Technology Act, 2000",
        "chapters": 13
    },
    "PWDVA": {
        "name": "Protection of Women from Domestic Violence Act",
        "year": 2005,
        "description": "Law protecting women from domestic violence",
        "fullForm": "Protection of Women from Domestic Violence Act, 2005",
        "chapters": 8
    },
    "POCSO": {
        "name": "Protection of Children from Sexual Offences Act",
        "year": 2012,
        "description": "Law protecting children from sexual abuse and exploitation",
        "fullForm": "Protection of Children from Sexual Offences Act, 2012",
        "chapters": 9
    },
    "NDPS": {
        "name": "Narcotic Drugs and Psychotropic Substances Act",
        "year": 1985,
        "description": "Law governing drug-related offenses",
        "fullForm": "Narcotic Drugs and Psychotropic Substances Act, 1985",
        "chapters": 6
    },
    "SC_ST_ACT": {
        "name": "Scheduled Castes and Scheduled Tribes (Prevention of Atrocities) Act",
        "year": 1989,
        "description": "Law preventing atrocities against SC/ST communities",
        "fullForm": "SC/ST (Prevention of Atrocities) Act, 1989",
        "chapters": 5
    },
    "MV_ACT": {
        "name": "Motor Vehicles Act",
        "year": 1988,
        "description": "Law governing motor vehicle offenses including accident and rash driving",
        "fullForm": "Motor Vehicles Act, 1988 (Amended 2019)",
        "chapters": 14
    }
}

# ────────────────────────────────────────────────────────────────────────────
#  LAW SECTIONS — Comprehensive database
# ────────────────────────────────────────────────────────────────────────────
LAW_SECTIONS = {
    # ═══════════════════  MURDER & HOMICIDE  ═══════════════════
    "BNS_100": {
        "act": "BNS", "section": "100", "title": "Culpable Homicide",
        "description": "Whoever causes death by doing an act with the intention of causing death, or with the intention of causing such bodily injury as is likely to cause death, or with the knowledge that he is likely by such act to cause death, commits the offence of culpable homicide.",
        "punishment": "Depends on whether it amounts to murder (Section 101) or not (Section 104).",
        "essentials": ["Causing death", "Intention or knowledge"],
        "defenses": ["Accident", "Insanity", "Self-defense"]
    },
    "BNS_101": {
        "act": "BNS", "section": "101", "title": "Murder",
        "description": "Whoever causes death of any person with the intention of causing death, or with the intention of causing such bodily injury as the offender knows to be likely to cause the death of the person, or with the intention of causing bodily injury sufficient in the ordinary course of nature to cause death, or knowing that the act is so imminently dangerous that it must in all probability cause death, commits murder.",
        "punishment": "Death or imprisonment for life, and shall also be liable to fine. The Court shall state special reasons if the sentence of death is not imposed.",
        "essentials": ["Intention to cause death", "Knowledge that act will likely cause death", "Bodily injury sufficient to cause death in ordinary course of nature"],
        "defenses": ["Grave and sudden provocation", "Private defense exceeding right", "Exercise of legal power in good faith", "Death caused in sudden fight without premeditation", "Consent of victim (age 18+)"]
    },
    "BNS_103": {
        "act": "BNS", "section": "103", "title": "Punishment for Murder",
        "description": "Whoever commits murder shall be punished with death or imprisonment for life and shall also be liable to fine.",
        "punishment": "Death penalty or life imprisonment, and fine. In cases involving repeat offenders or heinous circumstances, the death penalty may be imposed.",
        "essentials": ["Commission of murder as defined under Section 101"],
        "defenses": ["As per exceptions under Section 101 BNS"]
    },
    "BNS_104": {
        "act": "BNS", "section": "104", "title": "Culpable Homicide not amounting to Murder",
        "description": "Whoever causes death by doing an act with the intention of causing death, or with the intention of causing such bodily injury as is likely to cause death, or with the knowledge that he is likely by such act to cause death, commits the offence of culpable homicide not amounting to murder, if the act falls under the exceptions.",
        "punishment": "Imprisonment for life, or imprisonment up to 10 years and fine. If the act is done with the knowledge that it is likely to cause death but without any intention, imprisonment up to 10 years and fine.",
        "essentials": ["Causing death", "Intention or knowledge of causing death", "Act falls under exceptions to murder"],
        "defenses": ["Sudden provocation", "Right of private defense", "Accident", "Insanity"]
    },
    "BNS_105": {
        "act": "BNS", "section": "105", "title": "Dowry Death",
        "description": "Where the death of a woman is caused by any burns or bodily injury or occurs otherwise than under normal circumstances within seven years of her marriage and it is shown that soon before her death she was subjected to cruelty or harassment by her husband or any relative of her husband for, or in connection with, any demand for dowry, such death shall be called dowry death.",
        "punishment": "Imprisonment not less than 7 years, extendable to imprisonment for life, and fine.",
        "essentials": ["Death within 7 years of marriage", "Death by burns/bodily injury or unnatural circumstances", "Cruelty or harassment in connection with dowry demand"],
        "defenses": ["No dowry demand", "Death by natural causes", "No cruelty shown"]
    },
    "BNS_109": {
        "act": "BNS", "section": "109", "title": "Attempt to Murder",
        "description": "Whoever does any act with the intention or knowledge of causing death, and such act, under the circumstances in which it is done, is likely to cause death, commits the offence of attempt to murder.",
        "punishment": "Imprisonment up to 10 years and fine. If hurt is caused, imprisonment up to life and fine.",
        "essentials": ["Act done with intention/knowledge of causing death", "Act capable of causing death"],
        "defenses": ["Lack of intention", "Self-defense", "Impossibility of success"]
    },
    "BNS_110": {
        "act": "BNS", "section": "110", "title": "Abetment of Suicide",
        "description": "If any person commits suicide, whoever abets the commission of such suicide, shall be punished. Includes instigating, conspiring, or aiding the person to commit suicide.",
        "punishment": "Imprisonment up to 10 years and fine.",
        "essentials": ["Person committed suicide", "Accused abetted (instigated/aided/conspired)", "Direct nexus between abetment and suicide"],
        "defenses": ["No abetment proved", "No direct link to suicide", "Mental illness of deceased"]
    },
    "BNS_111": {
        "act": "BNS", "section": "111", "title": "Organised Crime",
        "description": "Any continuing unlawful activity including kidnapping, robbery, vehicle theft, extortion, land grabbing, contract killing, economic offence, cyber crimes, trafficking of persons, drugs, weapons or illicit goods or services, committed by or on behalf of an organized crime syndicate.",
        "punishment": "Imprisonment for life and fine not less than ₹10,00,000. If organized crime results in death, death penalty or imprisonment for life and fine not less than ₹10,00,000.",
        "essentials": ["Continuing unlawful activity", "Committed on behalf of organized crime syndicate", "Use of violence, threat, or intimidation"],
        "defenses": ["Not part of syndicate", "Coercion", "Lack of knowledge"]
    },
    "BNS_112": {
        "act": "BNS", "section": "112", "title": "Petty Organised Crime",
        "description": "Any syndicate or group committing offences of theft, snatching, cheating, unauthorized selling of tickets, unauthorized betting or gambling, selling of public examination question papers.",
        "punishment": "Imprisonment from 1 to 7 years and fine.",
        "essentials": ["Group activity", "Petty criminal enterprise"],
        "defenses": ["Acting alone", "No syndicate involvement"]
    },
    "BNS_113": {
        "act": "BNS", "section": "113", "title": "Terrorist Act",
        "description": "Whoever does any act with intent to threaten or likely to threaten the unity, integrity, sovereignty, security, or economic security of India, or to strike terror or likely to strike terror in the people or any section of the people, by using bombs, dynamite, explosives, hazardous substances, firearms, or other lethal weapons.",
        "punishment": "Death penalty if terrorist act results in death; otherwise imprisonment for life and fine not less than ₹10,00,000.",
        "essentials": ["Intent to threaten sovereignty/security", "Use of lethal weapons/explosives", "Striking terror"],
        "defenses": ["No terrorist intent", "Coercion"]
    },

    # ═══════════════════  PHYSICAL ASSAULT & HURT  ═══════════════════
    "BNS_115": {
        "act": "BNS", "section": "115", "title": "Voluntarily causing hurt",
        "description": "Whoever voluntarily causes hurt to any person is said to commit the offence of voluntarily causing hurt.",
        "punishment": "Imprisonment up to 1 year and/or fine up to ₹10,000. If by dangerous weapons/means: imprisonment up to 3 years and fine.",
        "essentials": ["Voluntary action", "Cause hurt"],
        "defenses": ["Accident", "Self-defense", "Medical treatment"]
    },
    "BNS_117": {
        "act": "BNS", "section": "117", "title": "Voluntarily causing grievous hurt",
        "description": "Whoever voluntarily causes grievous hurt to any person. Grievous hurt includes emasculation, permanent privation of sight/hearing, fracture/dislocation of bone, hurt endangering life, inability to follow ordinary pursuits for 20+ days.",
        "punishment": "Imprisonment up to 7 years and fine. If by dangerous weapons: imprisonment up to 10 years and fine.",
        "essentials": ["Voluntary action", "Grievous hurt caused (fracture, permanent injury, etc.)"],
        "defenses": ["Self-defense", "Sudden provocation", "Accident"]
    },
    "BNS_118": {
        "act": "BNS", "section": "118", "title": "Causing hurt or grievous hurt by act endangering life",
        "description": "Whoever causes hurt to any person by doing an act so rashly or negligently as to endanger human life or the personal safety of others.",
        "punishment": "Imprisonment up to 3 months or fine up to ₹2,500 or both; for grievous hurt: imprisonment up to 6 months or fine up to ₹5,000.",
        "essentials": ["Rash or negligent act", "Endangering life", "Hurt caused"],
        "defenses": ["Due care exercised", "Unforeseeable accident"]
    },
    "BNS_121": {
        "act": "BNS", "section": "121", "title": "Causing hurt by means of poison with intent to commit offence",
        "description": "Whoever administers to or causes to be taken by any person any poison or any stupefying, intoxicating or unwholesome drug with intent to cause hurt.",
        "punishment": "Imprisonment up to 10 years and fine.",
        "essentials": ["Administration of poison/drug", "Intent to cause hurt/offence"],
        "defenses": ["Medical treatment", "Accidental intake"]
    },
    "BNS_122": {
        "act": "BNS", "section": "122", "title": "Wrongful restraint and wrongful confinement",
        "description": "Whoever voluntarily obstructs any person so as to prevent that person from proceeding in any direction in which that person has a right to proceed, is said to wrongfully restrain that person. Wrongful confinement is keeping someone in a bounded area.",
        "punishment": "For wrongful restraint: imprisonment up to 1 month or fine up to ₹5,000 or both. For wrongful confinement: imprisonment up to 1 year or fine up to ₹5,000 or both.",
        "essentials": ["Voluntary obstruction", "Prevention of lawful movement"],
        "defenses": ["Legal authority", "Consent"]
    },
    "BNS_127": {
        "act": "BNS", "section": "127", "title": "Acid Attack",
        "description": "Whoever causes permanent or partial damage or deformity to, or burns or maims or disfigures or disables, any part or parts of the body of a person by throwing acid on or administering acid to that person.",
        "punishment": "Imprisonment not less than 10 years, extendable to imprisonment for life, and fine which shall be just and reasonable to meet the medical expenses of treatment.",
        "essentials": ["Throwing/administering acid", "Causing damage/disfigurement"],
        "defenses": ["Accident", "Self-defense"]
    },

    # ═══════════════════  SEXUAL OFFENSES  ═══════════════════
    "BNS_63": {
        "act": "BNS", "section": "63", "title": "Rape",
        "description": "A man is said to commit rape if he penetrates, manipulates, or applies his mouth or any body part to any woman under specified circumstances including against her will, without consent, with consent obtained by threat, etc.",
        "punishment": "Rigorous imprisonment not less than 10 years, extendable to life imprisonment, and fine.",
        "essentials": ["Without consent", "Against her will", "Consent obtained by fear/threat/impersonation"],
        "defenses": ["Consent freely given", "Marital exception (limited)"]
    },
    "BNS_64": {
        "act": "BNS", "section": "64", "title": "Punishment for Rape",
        "description": "Whoever commits rape shall be punished with rigorous imprisonment of either description for a term which shall not be less than ten years, but which may extend to imprisonment for life, and shall also be liable to fine.",
        "punishment": "Minimum 10 years RI, extendable to life imprisonment, and fine.",
        "essentials": ["Commission of rape as defined in Section 63"],
        "defenses": ["As per Section 63"]
    },
    "BNS_65": {
        "act": "BNS", "section": "65", "title": "Rape in certain cases (Aggravated Rape)",
        "description": "Rape by police officer, public servant, member of armed forces, hospital management/staff, person in position of trust or authority, during communal/sectarian violence, rape of pregnant woman, minor under 16, woman incapable of giving consent, or gang rape.",
        "punishment": "Rigorous imprisonment not less than 10 years, extendable to life imprisonment or death.",
        "essentials": ["Rape by person in authority", "Rape of minor/pregnant/disabled", "Gang rape"],
        "defenses": ["Consent", "Identity dispute"]
    },
    "BNS_66": {
        "act": "BNS", "section": "66", "title": "Rape of woman under 18 years",
        "description": "Whoever commits rape on a woman under eighteen years of age.",
        "punishment": "Rigorous imprisonment not less than 20 years, extendable to life (remainder of natural life), and fine.",
        "essentials": ["Victim under 18", "Sexual assault as defined in Section 63"],
        "defenses": ["Mistaken age (limited applicability)"]
    },
    "BNS_67": {
        "act": "BNS", "section": "67", "title": "Rape of woman under 12 years",
        "description": "Whoever commits rape on a woman under twelve years of age.",
        "punishment": "Rigorous imprisonment not less than 20 years, extendable to life or death, and fine.",
        "essentials": ["Victim under 12", "Sexual assault"],
        "defenses": ["Limited"]
    },
    "BNS_69": {
        "act": "BNS", "section": "69", "title": "Sexual intercourse by husband upon wife during separation",
        "description": "Whoever has sexual intercourse with his own wife, who is living separately, whether under a decree of separation or otherwise, without her consent.",
        "punishment": "Imprisonment up to 2 years and fine.",
        "essentials": ["Married couple living separately", "Without consent"],
        "defenses": ["Consent", "Cohabitation"]
    },
    "BNS_70": {
        "act": "BNS", "section": "70", "title": "Gang Rape",
        "description": "Where a woman is raped by one or more persons constituting a group or acting in furtherance of a common intention, each of such persons shall be deemed to have committed the offence of rape.",
        "punishment": "Rigorous imprisonment not less than 20 years, extendable to life (remainder of natural life), and fine.",
        "essentials": ["Multiple perpetrators", "Common intention", "Rape committed"],
        "defenses": ["Not part of group", "No common intention"]
    },
    "BNS_74": {
        "act": "BNS", "section": "74", "title": "Verbal and sexual harassment",
        "description": "Whoever, intending to insult the modesty of any person, utters any word, sound or makes any gesture, or exhibits any object.",
        "punishment": "Imprisonment up to 3 years and/or fine up to ₹10,000",
        "essentials": ["Intention to insult modesty", "Verbal/gesture harassment"],
        "defenses": ["No intention", "Mistake of fact"]
    },
    "BNS_75": {
        "act": "BNS", "section": "75", "title": "Sexual Harassment",
        "description": "A man committing any of the following acts: (i) physical contact and advances involving unwelcome and explicit sexual overtures; (ii) a demand or request for sexual favours; (iii) showing pornography against the will of a woman; (iv) making sexually coloured remarks.",
        "punishment": "Rigorous imprisonment up to 3 years, or fine, or both.",
        "essentials": ["Unwelcome sexual overtures", "Demand for sexual favours", "Showing pornography against will"],
        "defenses": ["Consent", "No sexual intent"]
    },
    "BNS_76": {
        "act": "BNS", "section": "76", "title": "Assault or use of criminal force to woman with intent to disrobe",
        "description": "Any man who assaults or uses criminal force to any woman or abets such act with the intention of disrobing or compelling her to be naked.",
        "punishment": "Imprisonment not less than 3 years, extendable to 7 years, and fine.",
        "essentials": ["Assault/criminal force", "Intent to disrobe"],
        "defenses": ["Accident", "No such intent"]
    },
    "BNS_78": {
        "act": "BNS", "section": "78", "title": "Voyeurism",
        "description": "Any man who watches or captures the image of a woman engaging in a private act in circumstances where she would usually have the expectation of not being observed.",
        "punishment": "First conviction: imprisonment not less than 1 year, extendable to 3 years, and fine. Second conviction: not less than 3 years, extendable to 7 years.",
        "essentials": ["Watching/capturing image", "Private act", "Without consent"],
        "defenses": ["Consent", "Public place"]
    },
    "BNS_79": {
        "act": "BNS", "section": "79", "title": "Stalking",
        "description": "Any man who follows a woman and contacts or attempts to contact such woman to foster personal interaction repeatedly despite a clear indication of disinterest by such woman; monitors the use of internet, email or any other form of electronic communication.",
        "punishment": "First conviction: imprisonment up to 3 years and fine. Second conviction: up to 5 years and fine.",
        "essentials": ["Repeated following/contact", "Clear indication of disinterest", "Monitoring communications"],
        "defenses": ["Lawful purpose", "Prevention of crime"]
    },

    # ═══════════════════  DOMESTIC VIOLENCE & CRUELTY  ═══════════════════
    "BNS_85": {
        "act": "BNS", "section": "85", "title": "Cruelty by husband or his relatives",
        "description": "Whoever, being the husband or the relative of the husband of a woman, subjects such woman to cruelty. Cruelty includes any wilful conduct which is of such a nature as is likely to drive the woman to commit suicide or to cause grave injury to life, limb or health (mental or physical). Also includes harassment with a view to coerce her or her relatives to meet any unlawful demand.",
        "punishment": "Imprisonment up to 3 years and fine.",
        "essentials": ["Wilful cruelty", "By husband or his relative", "Mental or physical harm", "Dowry-related harassment"],
        "defenses": ["No cruelty proved", "Mutual disputes"]
    },
    "BNS_86": {
        "act": "BNS", "section": "86", "title": "Woman abetment of suicide of minor or person of unsound mind",
        "description": "If any woman abets the suicide of a minor or a person of unsound mind.",
        "punishment": "Imprisonment up to 10 years and fine.",
        "essentials": ["Abetment", "Victim is minor or unsound mind", "Suicide occurred"],
        "defenses": ["No abetment", "No knowledge of mental state"]
    },

    # ═══════════════════  THEFT, ROBBERY & PROPERTY  ═══════════════════
    "BNS_303": {
        "act": "BNS", "section": "303", "title": "Theft",
        "description": "Whoever intends to take any movable property out of the possession of any person without that person's consent, in order to such property wrongfully to use it, is said to commit theft.",
        "punishment": "Imprisonment up to 3 years and/or fine up to ₹10,000",
        "essentials": ["Without consent", "Intention to wrongfully use", "Movable property"],
        "defenses": ["Mistake of fact", "Consent of owner"]
    },
    "BNS_304": {
        "act": "BNS", "section": "304", "title": "Snatching",
        "description": "Theft is snatching if the offender suddenly or quickly or forcibly seizes or secures or grabs or takes away from any person the movable property.",
        "punishment": "Imprisonment up to 3 years and fine.",
        "essentials": ["Sudden/quick force", "Seizing movable property"],
        "defenses": ["No force used", "Consent"]
    },
    "BNS_305": {
        "act": "BNS", "section": "305", "title": "Theft in dwelling house, vehicle, etc.",
        "description": "Whoever commits theft in any building, tent or vessel used as a human dwelling, or for custody of property; or of any vehicle, vessel, or place of worship.",
        "punishment": "Imprisonment up to 7 years and fine.",
        "essentials": ["Theft in dwelling/vehicle/place of worship"],
        "defenses": ["No entry", "Consent"]
    },
    "BNS_308": {
        "act": "BNS", "section": "308", "title": "Extortion",
        "description": "Whoever intentionally puts any person in fear of any injury and thereby dishonestly induces the person to deliver any property or valuable security or anything signed/sealed is said to commit extortion.",
        "punishment": "Imprisonment up to 3 years and/or fine up to ₹10,000",
        "essentials": ["Fear of injury", "Dishonest intention", "Delivery of property"],
        "defenses": ["No fear created", "No dishonest intention"]
    },
    "BNS_309": {
        "act": "BNS", "section": "309", "title": "Robbery",
        "description": "Theft accompanied by violence or threat of violence to person or property is robbery.",
        "punishment": "Imprisonment up to 10 years and/or fine up to ₹1,00,000",
        "essentials": ["Theft occurred", "Violence or threat", "Use of force"],
        "defenses": ["Self-defense", "Prevention of crime"]
    },
    "BNS_310": {
        "act": "BNS", "section": "310", "title": "Dacoity (Gang Robbery)",
        "description": "When five or more persons conjointly commit or attempt to commit a robbery, every person so committing, attempting or aiding is said to commit dacoity.",
        "punishment": "Imprisonment for life or rigorous imprisonment up to 10 years, and fine.",
        "essentials": ["Five or more persons", "Conjoint commission of robbery"],
        "defenses": ["Not part of group", "No common intention"]
    },
    "BNS_311": {
        "act": "BNS", "section": "311", "title": "Robbery or Dacoity with attempt to cause death or grievous hurt",
        "description": "If at the time of committing robbery or dacoity, the offender uses any deadly weapon, or causes grievous hurt.",
        "punishment": "Imprisonment for life or rigorous imprisonment not less than 7 years.",
        "essentials": ["Robbery/dacoity", "Deadly weapon used", "Grievous hurt caused"],
        "defenses": ["No weapon", "No grievous hurt"]
    },

    # ═══════════════════  FRAUD, CHEATING & FORGERY  ═══════════════════
    "BNS_315": {
        "act": "BNS", "section": "315", "title": "Cheating",
        "description": "Whoever by deceiving any person, fraudulently or dishonestly induces the person to deliver any property to any person, or to make, alter or destroy the whole or any part of a valuable security is said to cheat.",
        "punishment": "Imprisonment up to 3 years and/or fine.",
        "essentials": ["Deception", "Dishonest inducement", "Delivery of property"],
        "defenses": ["No deception", "Full disclosure"]
    },
    "BNS_316": {
        "act": "BNS", "section": "316", "title": "Cheating by personation",
        "description": "Whoever cheats by pretending to be some other person, or by knowingly substituting one person for another.",
        "punishment": "Imprisonment up to 5 years and fine.",
        "essentials": ["Impersonation", "Cheating through false identity"],
        "defenses": ["No impersonation", "Honest belief"]
    },
    "BNS_318": {
        "act": "BNS", "section": "318", "title": "Cheating and dishonestly inducing delivery of property",
        "description": "Whoever cheats and thereby dishonestly induces the person deceived to deliver any property.",
        "punishment": "Imprisonment up to 7 years and fine.",
        "essentials": ["Cheating", "Dishonest inducement", "Property delivery"],
        "defenses": ["No cheating", "Honest mistake"]
    },
    "BNS_319": {
        "act": "BNS", "section": "319", "title": "Forgery",
        "description": "Whoever makes any false document or false electronic record or part of a document or electronic record, with intent to cause damage or injury, or to support any claim or title, or to cause any person to part with property, commits forgery.",
        "punishment": "Imprisonment up to 2 years and fine. For valuable security: up to 7 years.",
        "essentials": ["False document created", "Intent to cause damage/injury", "Support false claim"],
        "defenses": ["No forgery", "No wrongful gain/loss"]
    },
    "BNS_320": {
        "act": "BNS", "section": "320", "title": "Forgery of valuable security, will, etc.",
        "description": "Whoever forges a document which purports to be a valuable security or a will, or an authority to adopt a son, or which purports to give authority to any person to make or transfer any valuable security.",
        "punishment": "Imprisonment for life, or imprisonment up to 10 years, and fine.",
        "essentials": ["Forging valuable security/will", "Intent to defraud"],
        "defenses": ["Genuine document", "No intent to defraud"]
    },
    "BNS_336": {
        "act": "BNS", "section": "336", "title": "Criminal Breach of Trust",
        "description": "Whoever, being in any manner entrusted with property, dishonestly misappropriates or converts it to his own use, or dishonestly uses or disposes of that property in violation of any direction of law or legal contract.",
        "punishment": "Imprisonment up to 5 years and fine. By public servant/banker/agent: up to 10 years.",
        "essentials": ["Entrusted with property", "Dishonest misappropriation"],
        "defenses": ["Honest mistake", "No dishonest intention"]
    },

    # ═══════════════════  KIDNAPPING & ABDUCTION  ═══════════════════
    "BNS_137": {
        "act": "BNS", "section": "137", "title": "Kidnapping",
        "description": "Whoever takes or entices any person from the keeping of the lawful guardian of such person, or from India, without the consent of such guardian, is said to kidnap.",
        "punishment": "Imprisonment up to 7 years and fine.",
        "essentials": ["Taking or enticing", "Without consent of guardian", "Minor or person of unsound mind"],
        "defenses": ["Consent of guardian", "Good faith action"]
    },
    "BNS_138": {
        "act": "BNS", "section": "138", "title": "Abduction",
        "description": "Whoever by force compels, or by any deceitful means induces, any person to go from any place, is said to abduct that person.",
        "punishment": "Punishment depends on purpose of abduction (see Sections 139-141).",
        "essentials": ["Force or deceit", "Compelling person to go from place"],
        "defenses": ["Consent", "Lawful authority"]
    },
    "BNS_139": {
        "act": "BNS", "section": "139", "title": "Kidnapping or abducting in order to murder",
        "description": "Whoever kidnaps or abducts any person in order that such person may be murdered or may be so disposed of as to be put in danger of being murdered.",
        "punishment": "Imprisonment for life or rigorous imprisonment up to 10 years, and fine.",
        "essentials": ["Kidnapping/abduction", "Intent to murder"],
        "defenses": ["No such intent"]
    },
    "BNS_140": {
        "act": "BNS", "section": "140", "title": "Kidnapping for ransom",
        "description": "Whoever kidnaps or abducts any person or keeps a person in detention after kidnapping and threatens to cause death or hurt, or demands ransom.",
        "punishment": "Death penalty or imprisonment for life, and fine.",
        "essentials": ["Kidnapping/detention", "Ransom demand", "Threat of death/hurt"],
        "defenses": ["No ransom demanded"]
    },
    "BNS_141": {
        "act": "BNS", "section": "141", "title": "Kidnapping or abducting for forced marriage/illicit intercourse",
        "description": "Whoever kidnaps or abducts any woman with intent that she may be compelled to marry any person against her will, or forced/seduced to illicit intercourse.",
        "punishment": "Imprisonment up to 10 years and fine.",
        "essentials": ["Kidnapping woman", "Intent to force marriage/intercourse"],
        "defenses": ["Consent", "Lawful marriage"]
    },

    # ═══════════════════  CRIMINAL INTIMIDATION & DEFAMATION  ═══════════════════
    "BNS_351": {
        "act": "BNS", "section": "351", "title": "Criminal Intimidation",
        "description": "Whoever threatens another with any injury to his person, reputation or property, or to the person or reputation of any one in whom that person is interested, with intent to cause alarm to that person.",
        "punishment": "Imprisonment up to 2 years, or fine, or both. If threat is of death or grievous hurt, imprisonment up to 7 years.",
        "essentials": ["Threat of injury", "Intent to cause alarm or coerce"],
        "defenses": ["No intent to alarm", "Lawful warning"]
    },
    "BNS_352": {
        "act": "BNS", "section": "352", "title": "Intentional insult with intent to provoke breach of peace",
        "description": "Whoever intentionally insults, and thereby gives provocation to any person, intending or knowing it to be likely that such provocation will cause him to break the public peace.",
        "punishment": "Imprisonment up to 2 years, or fine, or both.",
        "essentials": ["Intentional insult", "Intent to provoke breach of peace"],
        "defenses": ["No intent to provoke", "Fair comment"]
    },
    "BNS_356": {
        "act": "BNS", "section": "356", "title": "Defamation",
        "description": "Whoever, by words either spoken or intended to be read, or by signs or by visible representations, makes or publishes any imputation concerning any person intending to harm, or knowing or having reason to believe that such imputation will harm, the reputation of such person, is said to defame.",
        "punishment": "Simple imprisonment up to 2 years, or fine, or both.",
        "essentials": ["Imputation made or published", "Intent or knowledge of harming reputation"],
        "defenses": ["Truth for public good", "Public servant conduct", "Fair comment", "Court proceedings"]
    },

    # ═══════════════════  CYBERCRIME — IT ACT  ═══════════════════
    "IT_43": {
        "act": "IT_ACT", "section": "43", "title": "Unauthorized access to computer systems",
        "description": "If any person without permission of the owner accesses, downloads, copies, introduces virus, damages, disrupts, denies access to any computer, computer system or computer network.",
        "punishment": "Compensation by way of damages up to ₹5 crore.",
        "essentials": ["Unauthorized access", "Damage/disruption caused"],
        "defenses": ["Authorized access", "Accidental"]
    },
    "IT_66": {
        "act": "IT_ACT", "section": "66", "title": "Computer related offences (Hacking)",
        "description": "If any person, dishonestly or fraudulently, does any act referred to in section 43, he shall be punishable.",
        "punishment": "Imprisonment up to 3 years and/or fine up to ₹5,00,000.",
        "essentials": ["Dishonest/fraudulent act", "Computer-related offence"],
        "defenses": ["Authorization", "No dishonest intent"]
    },
    "IT_66A": {
        "act": "IT_ACT", "section": "66A", "title": "Punishment for sending offensive messages (Struck Down)",
        "description": "This section was struck down by the Supreme Court in Shreya Singhal v. Union of India (2015) as unconstitutional. Any prosecution under this section is void.",
        "punishment": "STRUCK DOWN — No punishment applicable.",
        "essentials": ["Section no longer valid"],
        "defenses": ["Section struck down by Supreme Court"]
    },
    "IT_66C": {
        "act": "IT_ACT", "section": "66C", "title": "Identity theft",
        "description": "Whoever, dishonestly or fraudulently make use of the electronic signature, password or any other unique identification feature of any other person.",
        "punishment": "Imprisonment up to 3 years and fine up to ₹1,00,000",
        "essentials": ["Fraudulent use", "Identity/password misuse"],
        "defenses": ["Authorization", "No fraudulent intent"]
    },
    "IT_66D": {
        "act": "IT_ACT", "section": "66D", "title": "Cheating by personation using computer resource",
        "description": "Whoever by means of any communication device or computer resource cheats by personation.",
        "punishment": "Imprisonment up to 3 years and fine up to ₹1,00,000",
        "essentials": ["Phishing/scam", "Personation"],
        "defenses": ["No deception", "Legitimate business"]
    },
    "IT_66E": {
        "act": "IT_ACT", "section": "66E", "title": "Punishment for violation of privacy",
        "description": "Whoever intentionally or knowingly captures, publishes or transmits the image of a private area of any person without his or her consent.",
        "punishment": "Imprisonment up to 3 years or fine up to ₹2,00,000 or both.",
        "essentials": ["Capturing private image", "Without consent", "Publishing/transmitting"],
        "defenses": ["Consent", "Public place"]
    },
    "IT_67": {
        "act": "IT_ACT", "section": "67", "title": "Publishing or transmitting obscene material in electronic form",
        "description": "Whoever publishes or transmits or causes to be published or transmitted in the electronic form, any material which is lascivious or appeals to the prurient interest.",
        "punishment": "First conviction: imprisonment up to 3 years and fine up to ₹5,00,000. Second conviction: up to 5 years and fine up to ₹10,00,000.",
        "essentials": ["Publishing obscene material", "Electronic form"],
        "defenses": ["Not obscene", "Public good"]
    },
    "IT_67A": {
        "act": "IT_ACT", "section": "67A", "title": "Publishing sexually explicit material in electronic form",
        "description": "Whoever publishes or transmits material containing sexually explicit act or conduct in electronic form.",
        "punishment": "First conviction: imprisonment up to 5 years and fine up to ₹10,00,000. Second conviction: up to 7 years and fine up to ₹10,00,000.",
        "essentials": ["Sexually explicit material", "Electronic publication"],
        "defenses": ["Consent of all depicted", "Not sexually explicit"]
    },
    "IT_67B": {
        "act": "IT_ACT", "section": "67B", "title": "Child pornography",
        "description": "Whoever publishes or transmits or creates or collects or seeks or browses or downloads or advertises child pornography in electronic form.",
        "punishment": "First conviction: imprisonment up to 5 years and fine up to ₹10,00,000. Second conviction: up to 7 years and fine up to ₹10,00,000.",
        "essentials": ["Child pornography", "Electronic form", "Any act related to child sexual material"],
        "defenses": ["Very limited — strict liability"]
    },

    # ═══════════════════  PROCEDURAL — BNSS  ═══════════════════
    "BNSS_173": {
        "act": "BNSS", "section": "173", "title": "Information in cognizable cases (FIR Registration)",
        "description": "Every information relating to the commission of a cognizable offence, if given orally or in writing to an officer in charge of a police station, shall be recorded and a copy given to the informant free of cost. This section also enables Zero FIR — a citizen may file an FIR at any police station regardless of jurisdiction.",
        "punishment": "N/A — Procedural provision governing the registration of FIRs",
        "essentials": ["Cognizable offence reported", "Information given orally or in writing", "Station officer records the information"],
        "defenses": ["N/A — This is a procedural right, not a penal section"]
    },
    "BNSS_187": {
        "act": "BNSS", "section": "187", "title": "Power to investigate cognizable cases",
        "description": "Any officer in charge of a police station may, without the order of a Magistrate, investigate any cognizable case which a Court having jurisdiction over the local area within the limits of such station would have power to inquire into or try.",
        "punishment": "N/A — Procedural provision",
        "essentials": ["Cognizable offence", "Police station within jurisdiction"],
        "defenses": ["N/A"]
    },
    "BNSS_479": {
        "act": "BNSS", "section": "479", "title": "Bail for non-bailable offences",
        "description": "When any person accused of, or suspected of, the commission of any non-bailable offence is arrested or detained, he may be released on bail. But the right is not automatic — court discretion applies. If investigation is not completed in 60 days (for offences punishable up to 7 years) or 90 days (for offences punishable with death/life/above 7 years), the accused gets default bail.",
        "punishment": "N/A — Procedural provision governing bail",
        "essentials": ["Non-bailable offence", "Arrested or detained", "Application before court"],
        "defenses": ["N/A"]
    },
    "BNSS_482": {
        "act": "BNSS", "section": "482", "title": "Direction for grant of anticipatory bail",
        "description": "When any person has reason to believe that he may be arrested on an accusation of having committed a non-bailable offence, he may apply to the High Court or the Court of Session for a direction that in the event of such arrest, he shall be released on bail.",
        "punishment": "N/A — Procedural provision governing anticipatory bail",
        "essentials": ["Apprehension of arrest", "Non-bailable offence", "Application to Sessions/High Court"],
        "defenses": ["N/A"]
    },

    # ═══════════════════  LEGACY IPC (for reference)  ═══════════════════
    "IPC_302": {
        "act": "IPC", "section": "302", "title": "Punishment for Murder",
        "description": "Whoever commits murder shall be punished with death, or imprisonment for life, and shall also be liable to fine.",
        "punishment": "Death or imprisonment for life, and fine.",
        "essentials": ["Intentional killing", "As defined under Section 300 IPC"],
        "defenses": ["Sudden provocation", "Self-defense", "Insanity"]
    },
    "IPC_304": {
        "act": "IPC", "section": "304", "title": "Culpable Homicide not amounting to Murder",
        "description": "Punishment for culpable homicide not amounting to murder.",
        "punishment": "Imprisonment for life, or imprisonment up to 10 years and fine.",
        "essentials": ["Causing death", "Falls under exceptions to murder"],
        "defenses": ["Sudden provocation", "Self-defense"]
    },
    "IPC_304A": {
        "act": "IPC", "section": "304A", "title": "Causing death by negligence",
        "description": "Whoever causes the death of any person by doing any rash or negligent act not amounting to culpable homicide.",
        "punishment": "Imprisonment up to 2 years, or fine, or both.",
        "essentials": ["Death caused", "Rash or negligent act", "Not culpable homicide"],
        "defenses": ["Due care exercised", "Unforeseeable"]
    },
    "IPC_304B": {
        "act": "IPC", "section": "304B", "title": "Dowry Death",
        "description": "Where the death of a woman is caused within seven years of marriage and it is shown that she was subjected to cruelty in connection with dowry demand.",
        "punishment": "Imprisonment not less than 7 years, extendable to life imprisonment.",
        "essentials": ["Death within 7 years of marriage", "Cruelty for dowry"],
        "defenses": ["Natural death", "No dowry demand"]
    },
    "IPC_307": {
        "act": "IPC", "section": "307", "title": "Attempt to Murder",
        "description": "Whoever does any act with such intention or knowledge, and under such circumstances that, if he by that act caused death, he would be guilty of murder.",
        "punishment": "Imprisonment up to 10 years, and fine. If hurt is caused, imprisonment for life.",
        "essentials": ["Intention or knowledge to cause death", "Act capable of causing death"],
        "defenses": ["No intention", "Self-defense", "Impossibility"]
    },
    "IPC_354": {
        "act": "IPC", "section": "354", "title": "Assault or criminal force to woman with intent to outrage modesty",
        "description": "Whoever assaults or uses criminal force to any woman, intending to outrage or knowing it to be likely that he will thereby outrage her modesty.",
        "punishment": "Imprisonment not less than 1 year, extendable to 5 years, and fine.",
        "essentials": ["Assault/force", "Intent to outrage modesty"],
        "defenses": ["Accident", "Medical/legal procedures"]
    },
    "IPC_376": {
        "act": "IPC", "section": "376", "title": "Punishment for Rape",
        "description": "Whoever commits rape as defined in Section 375 shall be punished.",
        "punishment": "Rigorous imprisonment not less than 10 years, extendable to life, and fine.",
        "essentials": ["Rape as defined in Section 375"],
        "defenses": ["Consent", "Mistaken identity"]
    },
    "IPC_379": {
        "act": "IPC", "section": "379", "title": "Theft",
        "description": "Whoever, intending to take dishonestly any movable property out of the possession of any person without that person's consent.",
        "punishment": "Imprisonment up to 3 years and/or fine.",
        "essentials": ["Without consent", "Dishonest intention"],
        "defenses": ["Mistake of fact", "Consent"]
    },
    "IPC_420": {
        "act": "IPC", "section": "420", "title": "Cheating and dishonestly inducing delivery of property",
        "description": "Whoever cheats and by means of such cheating dishonestly induces any person to deliver any property.",
        "punishment": "Imprisonment up to 7 years and fine.",
        "essentials": ["Cheating", "Dishonest inducement"],
        "defenses": ["No cheating", "Honest belief"]
    },
    "IPC_498A": {
        "act": "IPC", "section": "498A", "title": "Cruelty by husband or his relatives",
        "description": "Whoever, being the husband or the relative of the husband of a woman, subjects such woman to cruelty.",
        "punishment": "Imprisonment up to 3 years and fine.",
        "essentials": ["Cruelty", "Husband or relative"],
        "defenses": ["No cruelty", "Accidental"]
    },
    "IPC_506": {
        "act": "IPC", "section": "506", "title": "Criminal Intimidation",
        "description": "Whoever commits criminal intimidation shall be punished.",
        "punishment": "Imprisonment up to 2 years, or fine, or both. If threat of death/grievous hurt/fire/destruction: up to 7 years.",
        "essentials": ["Threat of injury", "Intent to cause alarm"],
        "defenses": ["No intent", "Lawful warning"]
    },

    # ═══════════════════  SPECIAL LAWS  ═══════════════════
    "POCSO_4": {
        "act": "POCSO", "section": "4", "title": "Punishment for penetrative sexual assault on child",
        "description": "Whoever commits penetrative sexual assault on a child.",
        "punishment": "Imprisonment not less than 10 years, extendable to life, and fine.",
        "essentials": ["Penetrative sexual act", "Victim is child (under 18)"],
        "defenses": ["Extremely limited"]
    },
    "POCSO_6": {
        "act": "POCSO", "section": "6", "title": "Aggravated penetrative sexual assault on child",
        "description": "Penetrative sexual assault by police/armed forces/public servant/relative/person in position of trust on a child; or gang penetrative sexual assault; or assault causing death/disability/pregnancy.",
        "punishment": "Rigorous imprisonment not less than 20 years, extendable to life (remainder of natural life) or death, and fine.",
        "essentials": ["Aggravating circumstances", "Victim is child"],
        "defenses": ["Very limited"]
    },
    "NDPS_20": {
        "act": "NDPS", "section": "20", "title": "Punishment for contravention in relation to cannabis plant and cannabis",
        "description": "Whoever in contravention of any provision of this Act or any rule or order or condition of licence: cultivates, produces, manufactures, possesses, sells, purchases, transports, imports, exports cannabis.",
        "punishment": "Small quantity: imprisonment up to 1 year or fine up to ₹10,000 or both. Less than commercial but more than small: imprisonment up to 10 years and fine up to ₹1,00,000. Commercial quantity: rigorous imprisonment not less than 10 years, extendable to 20 years, and fine not less than ₹1,00,000.",
        "essentials": ["Cannabis related contravention", "Possession/sale/transport"],
        "defenses": ["Personal consumption (small qty)", "Medical/scientific purpose"]
    },
    "NDPS_21": {
        "act": "NDPS", "section": "21", "title": "Punishment for contravention in relation to manufactured drugs",
        "description": "Whoever, in contravention of any provision of this Act or any rule: manufactures, possesses, sells, purchases, transports, imports, exports any manufactured drug or preparation.",
        "punishment": "Small quantity: imprisonment up to 1 year or fine up to ₹10,000 or both. Intermediate quantity: up to 10 years and fine up to ₹1,00,000. Commercial quantity: not less than 10 years, extendable to 20 years, and fine not less than ₹1,00,000.",
        "essentials": ["Manufactured drug contravention", "Possession/sale/transport"],
        "defenses": ["Planted evidence", "No knowledge of contents"]
    },
    "NDPS_22": {
        "act": "NDPS", "section": "22", "title": "Punishment for contravention in relation to psychotropic substances",
        "description": "Whoever, in contravention of any provision of this Act: manufactures, possesses, sells, purchases, transports, imports, exports any psychotropic substance.",
        "punishment": "Similar graded punishment as Section 20 and 21 based on quantity.",
        "essentials": ["Psychotropic substance", "Contravention"],
        "defenses": ["Lawful possession", "Medical use"]
    },
    "SC_ST_3": {
        "act": "SC_ST_ACT", "section": "3", "title": "Punishments for offences of atrocities",
        "description": "Whoever, not being a member of SC/ST, commits an offence under this section against a member of SC/ST including: forcing to eat or drink any inedible or obnoxious substance; dumping excreta/waste/carcasses; causing injury/insult/intimidation; wrongfully occupying land; forcing into bonded labour; intentionally insulting or intimidating with intent to humiliate in public view.",
        "punishment": "Imprisonment not less than 6 months, extendable to 5 years, and fine. For certain grave offences: not less than 1 year, extendable to life, and fine.",
        "essentials": ["Offender not SC/ST", "Victim is SC/ST", "Atrocity committed"],
        "defenses": ["No caste-based motive", "Factual dispute"]
    },
    "MV_184": {
        "act": "MV_ACT", "section": "184", "title": "Driving dangerously / Rash and negligent driving",
        "description": "Whoever drives a motor vehicle at a speed or in a manner which is dangerous to the public, having regard to all the circumstances of the case. Includes drunk driving.",
        "punishment": "First offence: imprisonment up to 6 months or fine up to ₹5,000 or both. Second offence within 3 years: imprisonment up to 2 years or fine up to ₹10,000 or both.",
        "essentials": ["Dangerous/rash driving", "Public risk"],
        "defenses": ["Emergency", "Mechanical failure"]
    },
    "MV_185": {
        "act": "MV_ACT", "section": "185", "title": "Driving by a drunken person or by a person under the influence of drugs",
        "description": "Whoever while driving a motor vehicle has in his blood alcohol exceeding 30mg per 100ml of blood detected in a test by a breath analyser.",
        "punishment": "First offence: imprisonment up to 6 months and/or fine up to ₹10,000. Second offence within 3 years: imprisonment up to 2 years and/or fine up to ₹15,000.",
        "essentials": ["Driving under influence", "BAC above limit"],
        "defenses": ["Faulty breathalyser", "Medical condition"]
    },
    "MV_304A_LINK": {
        "act": "BNS", "section": "106", "title": "Causing death by negligence (Road Accidents)",
        "description": "Whoever causes death of any person by doing any rash or negligent act not amounting to culpable homicide. If such death is caused by rash or negligent driving of a vehicle not amounting to culpable homicide and the person escapes without reporting, the punishment is enhanced.",
        "punishment": "Imprisonment up to 5 years and fine. If the person flees without reporting: imprisonment up to 10 years and fine.",
        "essentials": ["Death caused", "Rash/negligent driving", "Not culpable homicide"],
        "defenses": ["Due care", "Victim's negligence", "Mechanical failure"]
    },
}


# ────────────────────────────────────────────────────────────────────────────
#  CRIME-TO-SECTION MAPPING — Expanded
# ────────────────────────────────────────────────────────────────────────────
CRIME_TO_SECTIONS = {
    "Theft":             ["BNS_303", "BNS_304", "BNS_305", "IPC_379"],
    "Robbery":           ["BNS_309", "BNS_310", "BNS_311"],
    "CyberFraud":        ["BNS_315", "BNS_318", "IT_66", "IT_66C", "IT_66D"],
    "IdentityTheft":     ["IT_66C", "BNS_316", "BNS_319"],
    "Harassment":        ["BNS_74", "BNS_75", "BNS_79", "IPC_354", "BNS_351"],
    "SexualAssault":     ["BNS_63", "BNS_64", "BNS_65", "BNS_70", "BNS_74", "BNS_75", "IPC_354", "IPC_376"],
    "DomesticViolence":  ["BNS_85", "BNS_86", "BNS_105", "IPC_498A", "IPC_304B"],
    "Blackmail":         ["BNS_308", "BNS_351", "IPC_506"],
    "OnlineScams":       ["IT_66D", "IT_66", "BNS_315", "BNS_318"],
    "FinancialFraud":    ["BNS_315", "BNS_316", "BNS_336", "IPC_420"],
    "PhysicalAssault":   ["BNS_115", "BNS_117", "BNS_118", "BNS_127"],
    "Murder":            ["BNS_101", "BNS_103", "BNS_100", "BNS_104", "BNS_109", "IPC_302", "IPC_307"],
    "Kidnapping":        ["BNS_137", "BNS_138", "BNS_139", "BNS_140", "BNS_141"],
    "Defamation":        ["BNS_356", "BNS_352"],
    "DowryDeath":        ["BNS_105", "BNS_85", "IPC_304B", "IPC_498A"],
    "DrugOffenses":      ["NDPS_20", "NDPS_21", "NDPS_22"],
    "ChildAbuse":        ["POCSO_4", "POCSO_6", "BNS_66", "BNS_67", "IT_67B"],
    "Forgery":           ["BNS_319", "BNS_320"],
    "CriminalIntimidation": ["BNS_351", "BNS_352", "IPC_506"],
    "AcidAttack":        ["BNS_127", "BNS_117"],
    "DrunkenDriving":    ["MV_184", "MV_185", "MV_304A_LINK"],
    "RoadAccidentDeath": ["MV_304A_LINK", "MV_184", "BNS_104", "IPC_304A"],
    "OrganisedCrime":    ["BNS_111", "BNS_112"],
    "Terrorism":         ["BNS_113"],
    "CasteAtrocity":     ["SC_ST_3"],
    "Voyeurism":         ["BNS_78", "IT_66E"],
    "Stalking":          ["BNS_79"],
    "WrongfulConfinement": ["BNS_122"],
    "Poisoning":         ["BNS_121"],
    "Scam":              ["IT_66D", "BNS_318", "BNS_315"],
    "ConsumerRights":    ["BNS_315", "IPC_420"],
    "MissingPerson":     ["BNSS_173"],
    "LostDocument":      ["BNSS_173"],
    "GeneralInquiry":    ["BNSS_173", "BNSS_187", "BNSS_479", "BNSS_482"],
}


# ────────────────────────────────────────────────────────────────────────────
#  SAMPLE JUDGEMENTS — Comprehensive across all crime types
# ────────────────────────────────────────────────────────────────────────────
SAMPLE_JUDGEMENTS = [
    # ═══════════════════  MURDER  ═══════════════════
    {
        "id": "judgment_m01",
        "case_name": "Bachan Singh v. State of Punjab (1980)",
        "court": "Supreme Court of India",
        "year": 1980,
        "crime_type": "Murder",
        "legal_sections": ["IPC_302", "BNS_103"],
        "summary": "Landmark case establishing the 'rarest of rare' doctrine for imposing the death penalty. The Supreme Court held that the death penalty should only be imposed in the 'rarest of rare' cases when the alternative of life imprisonment is unquestionably foreclosed.",
        "key_findings": [
            "Death penalty is constitutional but should be used sparingly",
            "Courts must consider mitigating and aggravating circumstances",
            "The 'rarest of rare' test must be applied before sentencing death",
            "Life imprisonment is the rule, death penalty is the exception"
        ],
        "impact": "Established the foundational framework for death penalty jurisprudence in India.",
        "relevance_score": 99
    },
    {
        "id": "judgment_m02",
        "case_name": "Macchi Singh v. State of Punjab (1983)",
        "court": "Supreme Court of India",
        "year": 1983,
        "crime_type": "Murder",
        "legal_sections": ["IPC_302", "BNS_103"],
        "summary": "Further elaborated the 'rarest of rare' doctrine by providing categories where the death penalty may be warranted: manner of commission (extremely brutal/grotesque), motive (depravity), anti-social nature (victim is helpless), magnitude (multiple murders), and personality of victim (minor/old/woman).",
        "key_findings": [
            "Five categories for assessing death penalty: manner, motive, anti-social nature, magnitude, personality of victim",
            "Community's collective conscience must be shocked",
            "Balance sheet of aggravating and mitigating circumstances must be drawn"
        ],
        "impact": "Provided concrete guidelines for courts to assess when death penalty is warranted.",
        "relevance_score": 97
    },
    {
        "id": "judgment_m03",
        "case_name": "K.M. Nanavati v. State of Maharashtra (1962)",
        "court": "Supreme Court of India",
        "year": 1962,
        "crime_type": "Murder",
        "legal_sections": ["IPC_302", "BNS_101"],
        "summary": "Famous case involving a Naval Commander who killed his wife's lover. The Supreme Court rejected the defense of 'grave and sudden provocation' because there was a cooling-off period between learning of the affair and committing the murder. Established that planned/premeditated killing cannot claim provocation defense.",
        "key_findings": [
            "Provocation defense requires immediacy — no cooling-off period",
            "Premeditated murder cannot benefit from Exception 1 to Section 300 IPC / Section 101 BNS",
            "Last jury trial in Indian judicial history"
        ],
        "impact": "Defined strict boundaries for the 'provocation' defense in murder cases and led to abolition of jury trials in India.",
        "relevance_score": 95
    },
    {
        "id": "judgment_m04",
        "case_name": "Mukesh v. State (NCT of Delhi) — Nirbhaya Case (2017)",
        "court": "Supreme Court of India",
        "year": 2017,
        "crime_type": "Murder",
        "legal_sections": ["IPC_302", "IPC_376", "BNS_101", "BNS_63"],
        "summary": "The brutal gang-rape and murder case of December 2012 in Delhi that shook the nation. The Supreme Court upheld the death penalty for all four adult convicts, calling it the rarest of rare case. Led to the Criminal Law (Amendment) Act, 2013 which expanded the definition of rape and introduced death penalty for repeat offenders and rape causing death.",
        "key_findings": [
            "Death penalty upheld as the case met 'rarest of rare' standard",
            "Led to Criminal Law (Amendment) Act, 2013",
            "Expanded definition of rape under Indian law",
            "Introduced death penalty for rape causing death/persistent vegetative state"
        ],
        "impact": "Triggered sweeping criminal law reforms in India. Strengthened laws against sexual violence.",
        "relevance_score": 99
    },

    # ═══════════════════  SEXUAL ASSAULT  ═══════════════════
    {
        "id": "judgment_sa01",
        "case_name": "Vishaka v. State of Rajasthan (1997)",
        "court": "Supreme Court of India",
        "year": 1997,
        "crime_type": "SexualAssault",
        "legal_sections": ["BNS_75", "BNS_74"],
        "summary": "Landmark case on workplace sexual harassment. In the absence of legislation, the Supreme Court laid down guidelines (Vishaka Guidelines) to prevent and deal with sexual harassment at the workplace, which later formed the basis of the Sexual Harassment of Women at Workplace Act, 2013.",
        "key_findings": [
            "Defined sexual harassment at workplace",
            "Established mandatory complaint committee in every organization",
            "Laid down Vishaka Guidelines with force of law",
            "Led to POSH Act 2013"
        ],
        "impact": "Created the entire framework for sexual harassment law at workplaces in India.",
        "relevance_score": 98
    },
    {
        "id": "judgment_sa02",
        "case_name": "Tukaram v. State of Maharashtra — Mathura Rape Case (1979)",
        "court": "Supreme Court of India",
        "year": 1979,
        "crime_type": "SexualAssault",
        "legal_sections": ["IPC_376", "BNS_63"],
        "summary": "Controversial acquittal of two policemen accused of raping a tribal girl inside a police station. The court's reasoning that absence of injury meant consent was widely criticized and led to major amendments in rape law — shifting burden of proof to the accused in custodial rape cases.",
        "key_findings": [
            "Led to Criminal Law Amendment Act, 1983",
            "Introduced Section 114A — presumption of no consent in custodial rape",
            "Submission is not consent"
        ],
        "impact": "Triggered nationwide feminist movement and reformed India's rape laws fundamentally.",
        "relevance_score": 96
    },

    # ═══════════════════  THEFT & PROPERTY  ═══════════════════
    {
        "id": "judgment_t01",
        "case_name": "State v. Raj Kumar (2023)",
        "court": "Supreme Court of India",
        "year": 2023,
        "crime_type": "Theft",
        "legal_sections": ["BNS_303", "IPC_379"],
        "summary": "Landmark judgment on what constitutes theft in digital age. Court held that unauthorized transfer of digital assets falls under theft provisions.",
        "key_findings": [
            "Digital assets are movable property under BNS Section 303",
            "Intent to dishonestly take must be proved",
            "Possession of access credentials alone is not conclusive proof"
        ],
        "impact": "Modernized theft law to cover digital assets and cryptocurrency.",
        "relevance_score": 95
    },

    # ═══════════════════  DOMESTIC VIOLENCE  ═══════════════════
    {
        "id": "judgment_dv01",
        "case_name": "Sharma v. State (2022)",
        "court": "High Court of Delhi",
        "year": 2022,
        "crime_type": "DomesticViolence",
        "legal_sections": ["BNS_85", "IPC_498A"],
        "summary": "Important ruling on what constitutes cruelty in family matters. Court broadened definition to include emotional and mental abuse.",
        "key_findings": [
            "Mental cruelty is as punishable as physical cruelty",
            "Pattern of behavior matters more than individual incidents",
            "Cruelty need not be limited to physical violence"
        ],
        "impact": "Broadened the understanding of domestic cruelty to include emotional abuse.",
        "relevance_score": 92
    },
    {
        "id": "judgment_dv02",
        "case_name": "Arnesh Kumar v. State of Bihar (2014)",
        "court": "Supreme Court of India",
        "year": 2014,
        "crime_type": "DomesticViolence",
        "legal_sections": ["IPC_498A", "BNS_85"],
        "summary": "Supreme Court issued guidelines to prevent automatic arrests under Section 498A IPC (cruelty by husband). Police must follow a 9-point checklist before making arrests. Magistrates must not authorize detention without applying their mind. Aimed at preventing misuse of dowry harassment laws.",
        "key_findings": [
            "Police must satisfy 9-point checklist before arrest under 498A",
            "Magistrate must authorize detention carefully",
            "Aimed at preventing misuse of anti-dowry laws",
            "Non-compliance by police officers is punishable as contempt"
        ],
        "impact": "Protected against misuse of 498A while maintaining protection for genuine victims.",
        "relevance_score": 94
    },

    # ═══════════════════  DOWRY DEATH  ═══════════════════
    {
        "id": "judgment_dd01",
        "case_name": "Shanti v. State of Haryana (1991)",
        "court": "Supreme Court of India",
        "year": 1991,
        "crime_type": "DowryDeath",
        "legal_sections": ["IPC_304B", "BNS_105"],
        "summary": "Supreme Court clarified the scope of dowry death provision. Held that 'soon before death' does not mean immediately before death — there must be a proximate and live link between the cruelty/harassment and the death. The cruelty should be of such nature as to drive the woman to suicide or put her in a position where death occurs.",
        "key_findings": [
            "Proximate connection between cruelty and death required",
            "'Soon before death' is relative — not necessarily immediately before",
            "Continuous pattern of harassment sufficient",
            "Presumption under Section 113B of Evidence Act applies"
        ],
        "impact": "Clarified the evidentiary standards for proving dowry death cases.",
        "relevance_score": 93
    },

    # ═══════════════════  CYBER FRAUD  ═══════════════════
    {
        "id": "judgment_cf01",
        "case_name": "CBI v. Tech Fraudsters Gang (2023)",
        "court": "Supreme Court of India",
        "year": 2023,
        "crime_type": "CyberFraud",
        "legal_sections": ["BNS_315", "IT_66D"],
        "summary": "Comprehensive ruling on online fraud and phishing. Established guidelines for prosecution of cybercrime.",
        "key_findings": [
            "Phishing attacks fall under cheating provisions",
            "Collection of metadata is admissible evidence",
            "No consent needed for IP tracking in fraud investigation"
        ],
        "impact": "Created prosecution framework for modern cybercrime investigation.",
        "relevance_score": 98
    },
    {
        "id": "judgment_cf02",
        "case_name": "Shreya Singhal v. Union of India (2015)",
        "court": "Supreme Court of India",
        "year": 2015,
        "crime_type": "CyberFraud",
        "legal_sections": ["IT_66A"],
        "summary": "Landmark judgment striking down Section 66A of the IT Act as unconstitutional. The court held that the section was vague and overbroad, violating the right to free speech. However, it upheld Sections 69A (blocking websites) and 79 (intermediary liability with due diligence).",
        "key_findings": [
            "Section 66A struck down as unconstitutional — void ab initio",
            "Section 69A (blocking) upheld as constitutional with procedural safeguards",
            "Section 79 (intermediary liability) upheld with actual knowledge requirement",
            "Free speech online is a fundamental right"
        ],
        "impact": "Foundational judgment for internet freedom and free speech online in India.",
        "relevance_score": 97
    },

    # ═══════════════════  HARASSMENT  ═══════════════════
    {
        "id": "judgment_h01",
        "case_name": "Patel v. State (2021)",
        "court": "High Court of Mumbai",
        "year": 2021,
        "crime_type": "Harassment",
        "legal_sections": ["BNS_74", "IPC_354"],
        "summary": "Important judgment on workplace harassment. Clarified digital harassment and cyberbullying fall under harassment laws.",
        "key_findings": [
            "Digital harassment (messages, emails) falls under harassment sections",
            "Repeated unwanted contact is harassment even if not physically threatening",
            "Burden of proof on accused to show legitimate purpose"
        ],
        "impact": "Extended harassment laws to cover digital and online forms of harassment.",
        "relevance_score": 85
    },

    # ═══════════════════  KIDNAPPING  ═══════════════════
    {
        "id": "judgment_k01",
        "case_name": "Chhotu v. State of Rajasthan (2018)",
        "court": "Supreme Court of India",
        "year": 2018,
        "crime_type": "Kidnapping",
        "legal_sections": ["BNS_140", "BNS_137"],
        "summary": "Kidnapping for ransom case where the Supreme Court upheld the death sentence. Emphasized that kidnapping for ransom followed by murder of the victim is one of the most heinous crimes and warrants the severest punishment.",
        "key_findings": [
            "Kidnapping for ransom with murder is 'rarest of rare'",
            "Age of victim (child) is a significant aggravating factor",
            "Economic motive behind kidnapping does not mitigate"
        ],
        "impact": "Established that kidnapping for ransom with murder qualifies for death penalty.",
        "relevance_score": 92
    },

    # ═══════════════════  ROBBERY  ═══════════════════
    {
        "id": "judgment_r01",
        "case_name": "State of UP v. Ashok Kumar (2020)",
        "court": "Supreme Court of India",
        "year": 2020,
        "crime_type": "Robbery",
        "legal_sections": ["BNS_309", "BNS_311"],
        "summary": "Clarified the distinction between robbery and dacoity. Held that the use of a deadly weapon during robbery significantly enhances the gravity of the offense and warrants enhanced punishment under BNS Section 311.",
        "key_findings": [
            "Use of deadly weapon in robbery attracts enhanced punishment",
            "Distinction between robbery (individual/group <5) and dacoity (5+ persons)",
            "Victim's testimony is sufficient if corroborated by circumstances"
        ],
        "impact": "Provided clarity on weapon-aggravated robbery sentencing.",
        "relevance_score": 88
    },

    # ═══════════════════  DRUG OFFENSES  ═══════════════════
    {
        "id": "judgment_d01",
        "case_name": "Mohan Lal v. State of Punjab (2018)",
        "court": "Supreme Court of India",
        "year": 2018,
        "crime_type": "DrugOffenses",
        "legal_sections": ["NDPS_20", "NDPS_21"],
        "summary": "Supreme Court held that the complainant/informant police officer cannot be the investigating officer in NDPS cases. Any investigation where the complainant and IO are the same person vitiates the trial and the accused is entitled to acquittal.",
        "key_findings": [
            "Complainant police officer cannot be the Investigating Officer",
            "Separation of roles ensures fair investigation",
            "Violation of this principle vitiates the entire trial",
            "Acquittal is automatic if roles are merged"
        ],
        "impact": "Strengthened procedural safeguards in drug cases preventing police abuse.",
        "relevance_score": 95
    },
    {
        "id": "judgment_d02",
        "case_name": "Union of India v. Mohanlal (2016)",
        "court": "Supreme Court of India",
        "year": 2016,
        "crime_type": "DrugOffenses",
        "legal_sections": ["NDPS_20", "NDPS_21", "NDPS_22"],
        "summary": "Elaborated on the requirement of strict compliance with Section 42 and 50 of NDPS Act for search and seizure. Non-compliance with these mandatory procedural safeguards renders the seizure and subsequent conviction invalid.",
        "key_findings": [
            "Section 42 (search without warrant) and Section 50 (search of person) are mandatory",
            "Non-compliance vitiates the prosecution case",
            "Independent witnesses are important in NDPS seizures",
            "Conscious possession must be proved"
        ],
        "impact": "Protected accused persons from procedural irregularities in drug seizure cases.",
        "relevance_score": 93
    },

    # ═══════════════════  CHILD ABUSE / POCSO  ═══════════════════
    {
        "id": "judgment_ca01",
        "case_name": "Attorney General for India v. Satish (2021)",
        "court": "Supreme Court of India",
        "year": 2021,
        "crime_type": "ChildAbuse",
        "legal_sections": ["POCSO_4", "POCSO_6"],
        "summary": "Supreme Court overruled the Bombay High Court's controversial ruling that skin-to-skin contact was necessary for sexual assault under POCSO. Held that the most important ingredient is the sexual intent and not the skin-to-skin contact. Groping over clothes constitutes sexual assault.",
        "key_findings": [
            "Skin-to-skin contact NOT required to constitute sexual assault",
            "Sexual intent is the determining factor",
            "Groping over clothes is sexual assault under POCSO",
            "POCSO must be interpreted purposively to protect children"
        ],
        "impact": "Broadened the protection for children under POCSO and prevented narrow interpretations.",
        "relevance_score": 97
    },

    # ═══════════════════  DEFAMATION  ═══════════════════
    {
        "id": "judgment_def01",
        "case_name": "Subramanian Swamy v. Union of India (2016)",
        "court": "Supreme Court of India",
        "year": 2016,
        "crime_type": "Defamation",
        "legal_sections": ["BNS_356", "IPC_499"],
        "summary": "Supreme Court upheld the constitutional validity of criminal defamation. Held that reputation is a part of Article 21 (right to life) and criminal defamation serves as a reasonable restriction on free speech under Article 19(2).",
        "key_findings": [
            "Criminal defamation is constitutionally valid",
            "Right to reputation is part of right to life (Article 21)",
            "Defamation is a reasonable restriction on free speech",
            "Truth as defense must be for public good"
        ],
        "impact": "Settled the debate on constitutionality of criminal defamation in India.",
        "relevance_score": 90
    },

    # ═══════════════════  FINANCIAL FRAUD  ═══════════════════
    {
        "id": "judgment_ff01",
        "case_name": "Guru Ashish Construction v. Rajan Kumar (2023)",
        "court": "Supreme Court of India",
        "year": 2023,
        "crime_type": "FinancialFraud",
        "legal_sections": ["IPC_420", "BNS_315", "BNS_316"],
        "summary": "Dealt with cheating in real estate — builder collected money promising flats but neither delivered possession nor returned money. Court held that making false promises at inception of contract with no intention to perform constitutes cheating under BNS 315/IPC 420.",
        "key_findings": [
            "False promise at inception of contract is cheating",
            "Intent to deceive must exist at the time of making promise",
            "Subsequent failure to perform may not always be cheating — intent is key",
            "Both criminal and civil remedies available"
        ],
        "impact": "Clarified the distinction between breach of contract and criminal cheating.",
        "relevance_score": 88
    },

    # ═══════════════════  ACID ATTACK  ═══════════════════
    {
        "id": "judgment_aa01",
        "case_name": "Laxmi v. Union of India (2014)",
        "court": "Supreme Court of India",
        "year": 2014,
        "crime_type": "AcidAttack",
        "legal_sections": ["BNS_127"],
        "summary": "Landmark case on acid attacks. The Supreme Court directed regulation of sale of acid, ordered compensation of at least ₹3 lakh to acid attack victims, and directed states to ensure proper investigation and speedy trial. Victim Laxmi Agarwal became a symbol of strength and led to Criminal Law Amendment Act 2013 introducing Section 326A/326B IPC (now BNS 127).",
        "key_findings": [
            "Minimum ₹3 lakh compensation to acid attack victims",
            "Regulation of acid sale — mandatory ID proof",
            "Led to specific acid attack sections in criminal law",
            "States must provide free medical treatment"
        ],
        "impact": "Created comprehensive legal framework for acid attack prevention and victim support.",
        "relevance_score": 95
    },

    # ═══════════════════  ROAD ACCIDENT DEATH  ═══════════════════
    {
        "id": "judgment_rad01",
        "case_name": "State of Gujarat v. Haidarali Kalubhai (2021)",
        "court": "Supreme Court of India",
        "year": 2021,
        "crime_type": "RoadAccidentDeath",
        "legal_sections": ["IPC_304A", "MV_304A_LINK"],
        "summary": "Supreme Court upheld conviction for death caused by rash and negligent driving. Held that driving at excessive speed in a residential area, especially near schools and markets, constitutes 'rash and negligent driving' sufficient for conviction under Section 304A IPC / BNS 106.",
        "key_findings": [
            "Excessive speed in residential area is rash driving",
            "Death caused by negligent driving attracts criminal liability",
            "Compensation must be awarded to victim's family",
            "Driver has duty to slow down near schools, hospitals, markets"
        ],
        "impact": "Strengthened accountability for rash driving causing death.",
        "relevance_score": 87
    },

    # ═══════════════════  BLACKMAIL / EXTORTION  ═══════════════════
    {
        "id": "judgment_bl01",
        "case_name": "Romesh Chandra Arora v. State (1960)",
        "court": "Supreme Court of India",
        "year": 1960,
        "crime_type": "Blackmail",
        "legal_sections": ["BNS_308", "BNS_351"],
        "summary": "Supreme Court defined the essential elements of extortion: putting a person in fear of injury, and dishonestly inducing the person so put in fear to deliver property. The fear must be of such nature as to unsettle the mind of the person threatened.",
        "key_findings": [
            "Fear must unsettle the mind of the threatened person",
            "Delivery of property must be induced by fear",
            "Threat may be express or implied",
            "Both the threatening and the delivery constitute the offense"
        ],
        "impact": "Defined the foundational elements of extortion/blackmail under Indian law.",
        "relevance_score": 85
    },

    # ═══════════════════  IDENTITY THEFT  ═══════════════════
    {
        "id": "judgment_it01",
        "case_name": "State of Tamil Nadu v. Suhas Katti (2004)",
        "court": "Additional Chief Metropolitan Magistrate, Chennai",
        "year": 2004,
        "crime_type": "IdentityTheft",
        "legal_sections": ["IT_66C", "IT_66D"],
        "summary": "One of the first convictions under the IT Act. The accused created a fake Yahoo profile of the victim and posted obscene messages using her identity, causing harassment. Court convicted under IT Act Sections for identity theft and obscene publication.",
        "key_findings": [
            "Creating fake profiles constitutes identity theft",
            "Online impersonation is a criminal offense",
            "Electronic evidence is admissible",
            "Fast-track trial of cybercrime cases emphasized"
        ],
        "impact": "First major IT Act conviction; established precedent for cybercrime prosecution in India.",
        "relevance_score": 90
    },

    # ═══════════════════  SELF-DEFENSE  ═══════════════════
    {
        "id": "judgment_sd01",
        "case_name": "Darshan Singh v. State of Punjab (2010)",
        "court": "Supreme Court of India",
        "year": 2010,
        "crime_type": "PhysicalAssault",
        "legal_sections": ["BNS_115", "BNS_117"],
        "summary": "Supreme Court elaborated on the right of private defense. Held that the right of private defense is a right to defend and not to punish. The force used must be proportionate to the threat, and the right extends to causing death only if there is a reasonable apprehension of death or grievous hurt.",
        "key_findings": [
            "Right of private defense is to defend, not to punish",
            "Force must be proportionate to the threat",
            "Right extends to causing death only if apprehension of death/grievous hurt",
            "No right of private defense against lawful acts"
        ],
        "impact": "Clarified the scope and limits of the right to self-defense in Indian criminal law.",
        "relevance_score": 91
    },
]


# ────────────────────────────────────────────────────────────────────────────
#  UTILITY FUNCTIONS
# ────────────────────────────────────────────────────────────────────────────
def get_legal_section(section_code: str) -> dict:
    return LAW_SECTIONS.get(section_code)

def get_sections_for_crime(crime_type: str) -> list:
    return CRIME_TO_SECTIONS.get(crime_type, [])

def search_sections(keyword: str, act: str = None) -> list:
    results = []
    for code, section in LAW_SECTIONS.items():
        if act and section.get("act") != act:
            continue
        if keyword.lower() in section.get("title", "").lower() or \
           keyword.lower() in section.get("description", "").lower():
            results.append({"code": code, **section})
    return results

def search_judgements(keyword: str = None, crime_type: str = None) -> list:
    results = []
    for judgment in SAMPLE_JUDGEMENTS:
        if crime_type and judgment.get("crime_type") != crime_type:
            continue
        if keyword and keyword.lower() not in judgment.get("case_name", "").lower() and \
           keyword.lower() not in judgment.get("summary", "").lower():
            continue
        results.append(judgment)
    return results

def get_judgement_by_id(judgment_id: str) -> dict:
    for j in SAMPLE_JUDGEMENTS:
        if j["id"] == judgment_id:
            return j
    return None

def semantic_search_judgements(query: str) -> list:
    """
    Search judgements by keyword matching.
    Falls back to simple keyword search from the static knowledge base.
    """
    return search_judgements(keyword=query)

