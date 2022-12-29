[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9434298&assignment_repo_type=AssignmentRepo)
# CSC3170 Course Project

## Project Overall Description

This is our implementation for the course project of CSC3170, 2022 Fall, CUHK(SZ). For details of the project, you can refer to [project-description.md](project-description.md). In this project, we will utilize what we learned in the lectures and tutorials in the course, and implement either one of the following major jobs:

<!-- Please fill in "x" to replace the blank space between "[]" to tick the todo item; it's ticked on the first one by default. -->

- [ ] **Application with Database System(s)**
- [x] **Implementation of a Database System**

## Project Material:
- Presentation Video:
  - Our group recorded a video to explain the design logic of our DBMS and demonstrate the case.
  - [The video link of Bilibili](https://www.bilibili.com/video/BV1u3411X7bv/?vd_source=51a38500fd91532549e8cb917491cc06)
  - [The video link of Youtube](https://www.youtube.com/watch?v=qNXOF0NTCUs) 
- Presentation Slides:
  - You can check the [presentation slides](https://github.com/CSC3170-2022Fall/project-team10/blob/main/Project's%20Presentation%20Slide.pdf)
- Detailed project report:
  - You can check the detailed implementation and design in this [report](CSC3170_Project_Report.pdf)
- The whole database code and sample of .db files are involved in [option3](option3)
  - You simply need to run the [main.py](option3/main.py) to enter the user interface of DBMS
  - We provided some [testcase](testcase.pdf) to test our database
  


## Team Members

Our team consists of the following members, listed in the table below (the team leader is shown in the first row, and is marked with 🚩 behind his/her name):

<!-- change the info below to be the real case -->

| Student ID | Student Name | GitHub Account (in Email) |
| ---------- | ------------ | ------------------------- |
| 120090545  | 李佳齐 🚩 (Github name: AnakinSkywalker603)    | 120090545@link.cuhk.edu.cn |
| 119010289  | 万茜(Github name: Eggy-6)         | 119010289@link.cuhk.edu.cn |
| 120090674  | 张泽萱(Github name: Gila-6)        | 120090674@link.cuhk.edu.cn |
| 120090133  | 徐康裕(Github name: Barrxxx)        | 120090133@link.cuhk.edu.cn |
| 120090533  | 周泽睿        | 120090533@link.cuhk.edu.cn |
| 120090311  | 樊天宇(Github name: 120090311)        | 120090311@link.cuhk.edu.cn |
| 120090597  | 孙鑫昊        | 120090597@link.cuhk.edu.cn |

## Project Specification

<!-- You should remove the terms/sentence that is not necessary considering your option/branch/difficulty choice -->

After thorough discussion, our team made the choice and the specification information is listed below:

- Our option choice is: **Option 3**


## Project Abstract
Our goal of this project is to simulate a simplified relational database management system (DBMS), which is option 3 of the course project. This simplified DBMS can handle the basic tasks of a typical DBMS. The users can interact with this simplified DBMS using SQL commands.

To complete the test, our group uses python to develop this project. The source code of this project is divided into several python files. These files includes one main file, which will be executed by the user to start the interaction with the DBMS, one interpreter file, which interpret the commands the users put in the terminal, and other files to handle each type of commands.

If the project is developed successfully, the users can interact with this DBMS through typing SOL commands into the terminal. The DBMS can interpret these commands and do the corresponding operations. The data managed by this DBMS will be stored in .db files.

## Other Material
This is the [open source license](licence) for project
<!-- TODO -->

## Project Report
Please check this [pdf](CSC3170_Project_Report.pdf) file.
