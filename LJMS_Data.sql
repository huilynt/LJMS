SET GLOBAL local_infile=1;

USE ljps;

-- LMS Course
LOAD DATA INFILE  'C:/wamp64/tmp/RawData/courses.csv'
INTO TABLE Course
CHARACTER SET latin1
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

-- LMS Role
LOAD DATA INFILE  'C:/wamp64/tmp/RawData/role.csv'
INTO TABLE Role
CHARACTER SET latin1
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

-- LMS Staff
LOAD DATA INFILE  'C:/wamp64/tmp/RawData/staff.csv'
INTO TABLE Staff
CHARACTER SET latin1
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

-- LMS Registration
LOAD DATA INFILE  'C:/wamp64/tmp/RawData/registration.csv'
INTO TABLE Registration
CHARACTER SET latin1
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

-- LJPS Job Role
insert into JobRole (JobRole_ID, JobRole_Name, JobRole_Desc) values 
('DA001', 'Data Analyst', 'The role requires you to make recommendations about the methods and ways in which a company obtains and analyses data to improve quality and the efficiency of data systems.'),
('VE001', 'Video Editor', 'The role is to manage material such as camera footage, dialogue, sound effects, graphics and special effects to produce a final film or video product.'),
('EN001', 'Software Engineer', 'The role focus on applying the principles of engineering to software development.'),
('EN002', 'DevOps Engineer', 'It is an IT generalist who should have a wide-ranging knowledge of both development and operations, including coding and infrastructure management.'),
('PM001', 'Project Manager', 'The role is responsible for planning, organizing, and directing the completion of specific projects for an organization while ensuring these projects are on time, on budget, and within scope'),
('HR001', 'Employee Relations Manager', 'The role maintains a harmonious work environment by addressing certain behaviors that affect the workplace.'),
('CO001', 'C-level Executive', 'Play a strategic role within an organization; they hold senior positions and impact company-wide decisions'),
('EC001', 'Environmental Consultant', 'Support and implement programs that focus on improving the environment, saving money for their employer, and helping their local community.')
;


-- LJPS Skill
insert into Skill (Skill_ID, Skill_Name, Skill_Desc) values
('DM01', 'Data Mining', 'Comprises all disciplines related to managing data as a valuable resource'),
('PG01', 'Photography', 'The art or practice of taking and processing photographs.'),
('RM01', 'Risk Management', 'The identification, evaluation, and prioritization of risks followed by coordinated and economical application of resources to minimize, monitor, and control the probability or impact of unfortunate events or to maximize the realization of opportunities'),
('SM01', 'Service Management', 'It is the activities that are performed by an organization to design, build, deliver, operate and control information technology services offered to customers'),
('SD01', 'Software Development', 'It is to analyze users’ needs and then design, test, and develop software to meet those needs'),
('HR01', 'Human Resource Management', 'A strategic approach to the effective and efficient management of people in a company or organization such that they help their business gain a competitive advantage'),
('OR01', 'Organisation Skill', 'Creating structure and order, boosting productivity, and prioritizing tasks that must be completed immediately'),
('OR02', 'Organisation Culture', 'An culture defines the proper way to behave within the organization. It consists of shared beliefs and values established by leaders and communicated and reinforced through various methods, shaping employee perceptions, behaviors and understanding'),
('LE01', 'Leadership Skill', 'How to be a leader'),
('BM01', 'Brand Management', 'Analysis on how a brand is currently perceived in the market, proceeds to planning how the brand should be perceived'),
('LE02', 'Leadership Management', 'The process of planning, organizing, directing, and controlling the activities of employees in combination with other resources to accomplish organizational objectives.'),
('CM01', 'Change Management', 'For all approaches to prepare, support, and help individuals, teams, and organizations in making organizational change.'),
('SS01', 'Corporate Sustainability', 'An approach aiming to create long-term stakeholder value through the implementation of a business strategy that focuses on the ethical, social, environmental'),
('PS01', 'Problem Solving', 'The process of achieving a goal by overcoming obstacles, a frequent part of most activities')
;

-- LJPS JobRole_Skill
insert into JobRole_Skill (JobRole_ID, Skill_ID) values
('DA001', 'DM01'),
('VE001', 'PG01'),
('EN001', 'SD01'),
('EN002', 'SD01'),
('EN002', 'SM01'),
('EN002', 'RM01'),
('PM001', 'HR01'),
('PM001', 'LE01'),
('PM001', 'BM01'),
('PM001', 'CM01'),
('HR001', 'HR01'),
('HR001', 'BM01'),
('EN002', 'OR01'),
('CO001', 'LE02'),
('CO001', 'OR02'),
('CO001', 'OR01'),
('EC001', 'SS01'),
('EC001', 'PS01')
;

-- LJPS Skill_Course 
insert into Skill_Course (Skill_ID, Course_ID) values
('SD01', 'COR001'),  
('RM01', 'COR002'),
('BM01', 'COR002'), 
('SM01', 'COR002'),
('SM01', 'COR004'), 
('RM01', 'COR006'), 
('SM01', 'COR006'), 
('DM01', 'FIN001'), 
('RM01', 'FIN002'), 
('OR01', 'FIN003'), 
('OR01', 'HRD001'),
('LE01', 'HRD001'),
('OR02', 'HRD001'),
('LE02', 'HRD001'),
('HR01', 'MGT001'),
('LE01', 'MGT001'),
('HR01', 'MGT002'),
('OR02', 'MGT002'),
('HR01', 'MGT003'),
('LE01', 'MGT004'),
('LE01', 'MGT007'),
('HR01', 'MGT007'),
('RM01', 'SAL001'),
('BM01', 'SAL003'),
('LE01', 'SAL004'),
('HR01', 'SAL004'),
('PG01', 'tch003'),
('OR01', 'tch005'),
('RM01', 'tch008'),
('CM01', 'COR006'),
('CM01', 'tch019'),
('SS01', 'tch005'),
('PS01', 'MGT002'),
('PS01','tch018')
;

-- LJPS Learning Journey
insert into LearningJourney (Journey_ID, Staff_ID, JobRole_ID, LearningJourney_Status) values
('EN001-130001', 130001, 'EN001','Progress'),
('DA001-130001', 130001, 'DA001','Progress'),
('CO001-130002', 130002, 'CO001','Progress'),
('PM001-140001', 140001, 'PM001','Progress'),
('EN001-140525', 140525, 'EN001','Progress'),
('EN002-140525', 140525, 'EN002','Progress'), 
('PM001-140525', 140525, 'PM001','Progress'),
('CO001-150008', 150008, 'CO001','Progress'),
('PM001-150115', 150115, 'PM001','Progress'),
('EC001-150115', 150115, 'EC001','Progress'),
('EN002-150166', 150166, 'EN002','Progress'),
('DA001-150166', 150166, 'DA001','Progress'),
('EC001-160065', 160065, 'EC001','Progress'),
('HR001-160212', 160212, 'HR001','Progress'), 
('EN001-160188', 160188, 'EN001','Progress'),
('DA001-170238', 170238, 'DA001','Progress')
;

-- LJPS LearningJourney_Course 
insert into LearningJourney_SelectedCourse (Journey_ID, Course_ID) values
('EN001-130001','COR001'),
('DA001-130001','FIN001'),
('CO001-130002','HRD001'),
('PM001-140001','MGT001'),
('PM001-140001','SAL004'),
('PM001-140001','COR006'), 
('EN001-140525','COR001'),
('EN002-140525','COR006'),
('PM001-140525','SAL004'),
('PM001-140525','tch002'),
('PM001-140525','MGT001'),
('PM001-150115','tch019'),
('EC001-150115','tch005'),
('EC001-150115','tch018'),
('EN002-150166','COR002'),
('DA001-150166','FIN001'),
('EN002-150166','tch005'),
('EC001-160065','MGT002'),
('EC001-160065','tch005'),
('HR001-160212','MGT001'),
('HR001-160212','COR002'),
('EN001-160188','COR001'),
('DA001-170238','FIN001')
;



