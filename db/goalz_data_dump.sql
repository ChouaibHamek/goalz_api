INSERT INTO "users" VALUES(1,'Chouaib',1362015937,'E6C5F49BD4DF062BC92419C7EA63806B');
INSERT INTO "users" VALUES(2,'Daniel',1357724086,'AA47F8215C6F30A0DCDB2A36A9F4168E');
INSERT INTO "users" VALUES(3,'Aleks',1362012937,'E59866DA313C462029662C2D9E9DE531');
INSERT INTO "users" VALUES(4,'Alfitra',1389260086,'604069857BBCD824F562249E062D35C1');
INSERT INTO "users" VALUES(5,'Jasmin',1394357686,'E9CB94C3D8205D025D5C9077EF15B6B7');
INSERT INTO "users" VALUES(6,'Bouteflika',1394357686,'255C8E8492E4C26868449941359ECEAC');

INSERT INTO "users_profile" VALUES(1,1,'Chouaib','Ha','c@h.com','https://github.com/ChouaibHamek', 24, 'M');
INSERT INTO "users_profile" VALUES(2,2,'Daniel','To','d@t.com','https://github.com/dtoniuc', 18, 'M');
INSERT INTO "users_profile" VALUES(3,3,'Aleks','Zi','a@z.com','https://www.linkedin.com/in/aleksandar-zhivkovic/', 19, 'M');
INSERT INTO "users_profile" VALUES(4,4,'Alfitra','Ra','a@r.com','https://www.linkedin.com/in/alfitra-rahman-00057151/', 19, 'M');
INSERT INTO "users_profile" VALUES(5,5,'Jasmin','he','h@h.com',NULL, 42, 'F');
INSERT INTO "users_profile" VALUES(6,6,'Bouteflika','pr','b@p.com',NULL, 89, 'M');

INSERT INTO "goals" VALUES(1, NULL,1,"Acquire citizenship",'Life, travel','You know',1519172121,0.7,1);
INSERT INTO "goals" VALUES(2,NULL,2,"Cross country ski",'sports','You know',1616199840,0.1,2);
INSERT INTO "goals" VALUES(3,2,2,"Learn Skating",'sports','You know',1550707200,0.99,2);
INSERT INTO "goals" VALUES(4,NULL,3,"Cross fit",'sports','You know',1584664200,1,3);
INSERT INTO "goals" VALUES(5,NULL,4,"piano and flute",'music','You know',1616199840,0.15,4);
INSERT INTO "goals" VALUES(6,NULL,5,"build rockets",'physics','You know',1740099600,0.22,5);
INSERT INTO "goals" VALUES(7,NULL,6,"extend life",'biology','You know',1561075200,0.88,6);
INSERT INTO "goals" VALUES(8,6,5,"learn physics",'physics','You know',1534291200,0.3,5);
INSERT INTO "goals" VALUES(9,8,5,"learn maths",'maths','You know',1526860800,0.0,5);

INSERT INTO "resources" VALUES(1,2,1,'How to use skies', 'https://www.tyrol.com/things-to-do/sports/cross-country-skiing/how-to-get-started', 'sports','Helpful if you are really into skiing',12,1);
INSERT INTO "resources" VALUES(2,4,2,'Cross fit best practices', 'https://breakingmuscle.com/fitness/the-formula-for-a-successful-crossfit-gym', 'sports','Key to success in crossfit',7,0.9);
INSERT INTO "resources" VALUES(3,1,3,'US citizenship requirement', 'https://www.uscis.gov/us-citizenship/citizenship-through-naturalization', 'life','US is an option, although the healthcare system maybe not as good',3,0.98);
INSERT INTO "resources" VALUES(4,5,4,'Flute techniques', 'https://www.vsl.co.at/en/Concert_flute/Playing_Techniques/', 'music','It helped me a lot to learn the basic and advanced techniques',40,0.85);
