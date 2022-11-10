SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+08:00";

CREATE DATABASE IF NOT EXISTS `LJPS`;
USE `LJPS`;

CREATE TABLE Role (
    Role_ID int NOT NULL,
    Role_Name varchar(20) NOT NULL,
    PRIMARY KEY (Role_ID)
);

CREATE TABLE Course (
    Course_ID varchar(20) NOT NULL,
    Course_Name varchar(50) NOT NULL,
    Course_Desc varchar(255),
    Course_Status varchar(15),
    Course_Type varchar(10),
    Course_Category varchar(50),
    PRIMARY KEY (Course_ID)
);

CREATE TABLE Staff (
    Staff_ID int NOT NULL,
    Staff_FName varchar(50) NOT NULL,
    Staff_LName varchar(50) NOT NULL,
    Dept varchar(50) NOT NULL,
    Email varchar(50) NOT NULL,
    Role int,
    PRIMARY KEY (Staff_ID),
    CONSTRAINT FK_RoleStaff FOREIGN KEY (Role) REFERENCES Role(Role_ID)
);

CREATE TABLE Registration (
    Reg_ID int NOT NULL,
    Course_ID varchar(20),
    Staff_ID int,
    Reg_Status varchar(20),
    Completion_Status varchar(20),
    PRIMARY KEY (Reg_ID),
    CONSTRAINT FK_CourseRegistration FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID),
    CONSTRAINT FK_StaffRegistration FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID)
);

CREATE TABLE JobRole (
    JobRole_ID varchar(20) NOT NULL,
    JobRole_Name varchar(50) NOT NULL,
    JobRole_Desc varchar(255),
    JobRole_Status varchar(20),
    PRIMARY KEY (JobRole_ID)
);

CREATE TABLE Skill (
    Skill_ID varchar(20) NOT NULL,
    Skill_Name varchar(50) NOT NULL,
    Skill_Desc varchar(255),
    Skill_Status varchar(20),
    PRIMARY KEY (Skill_ID)
);

CREATE TABLE JobRole_Skill (
    JobRole_ID varchar(20) NOT NULL,
    Skill_ID varchar(20) NOT NULL,
    CONSTRAINT PK_JobRole_Skill PRIMARY KEY (JobRole_ID,Skill_ID),
    CONSTRAINT FK_JobRole FOREIGN KEY (JobRole_ID) REFERENCES JobRole(JobRole_ID),
    CONSTRAINT FK_Skill FOREIGN KEY (Skill_ID) REFERENCES Skill(Skill_ID)
);

CREATE TABLE Skill_Course (
    Skill_ID varchar(20) NOT NULL, 
    Course_ID varchar(20) NOT NULL, 
    CONSTRAINT PK_Skill_Course PRIMARY KEY (Skill_ID, Course_ID),
    CONSTRAINT FK_Course FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID),
    CONSTRAINT FK_Skill_Course FOREIGN KEY (Skill_ID) REFERENCES Skill(Skill_ID)
);

CREATE TABLE LearningJourney(
    Journey_ID varchar(20) NOT NULL,
    Staff_ID int NOT NULL,
    JobRole_ID varchar(20) NOT NULL,
    LearningJourney_Status varchar(20), 
    PRIMARY KEY (Journey_ID),
    CONSTRAINT FK_LearningJourney_Staff FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID),
    CONSTRAINT FK_LearningJourney_JobRole FOREIGN KEY (JobRole_ID) REFERENCES JobRole(JobRole_ID)
);

CREATE TABLE LearningJourney_SelectedCourse (
    Journey_ID varchar(20) NOT NULL,
    Course_ID varchar(20) NOT NULL,
    CONSTRAINT Journey_ID_Course_ID PRIMARY KEY (Journey_ID, Course_ID),
    CONSTRAINT FK_LearningJourney_Course FOREIGN KEY (Journey_ID) REFERENCES LearningJourney(Journey_ID) ON DELETE CASCADE, 
    CONSTRAINT FK_Course_ID FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID) ON DELETE CASCADE
);