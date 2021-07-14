# Resume Parser
## _Automated Resume Screening_


Resume screening is the process of identifying if a candidate qualifies for a job by matching the requirements of the role with the information on their resumes such as education, skills, certifications, experience, and achievements. Resume screening is crucial to determine whether a candidate moves to the next stage of the hiring process or not, especially in high-volume application scenarios.

This repository uses Text mining and natural language processing algorithms for screening objectively thousands of resumes in a few minutes without bias to identify the best fit for a job opening based on thresholds, specific criteria or scores

## Folder structure for execution
```
- resume_scoring.py
- scripts
- Job_Description.txt
- skills.csv
- sample
   | Resume_1.pdf
   | Resume_2.pdf
    .
    .
    .
   | Resume_n.pdf
```
The resumes of the candidates should be in the ```sample``` folder. Currently the script only works with ```PDF/DOCX``` format.

## Local Setup

- Install Miniconda from the following [link](https://docs.conda.io/en/latest/miniconda.html)
- Create a new environment using the following commands
    ```
    conda create --name resume_parser -y
    conda activate resume_parser
    conda install pip -y
    conda update --all -y
    ```
- Set the root directory as Resume_Parser using ```cd Resume_Parser```
- Run ```pip install -r requirements.txt``` to install the libraries required to run the script

## Steps for executing the script

- There are two files ```Job_Description.txt``` and ```skills.csv``` which require manual intervention
- The recruiter/person using this script has to copy and paste the Job Description as it is in the ```Job_Description.txt``` file and save it
- Recruiter/person using this script has to paste the _Primary, Secondary_ skills in the _Primary, Secondary_ skills column in the ```skills.csv``` file respectively
- Once the above files are taken care of, paste all the resumes in the ```sample``` folder which are to be used for screening purposes
- Executing ```python resume_scoring.py``` will generate ```Candidates_score.csv``` file which is sorted in a descending order where the candidate with the highest score will be on the first row
- This file can then be viewed in a spreadsheet application to go through the relevant candidates

## Docker Setup and Execution instructions
- Install docker from their official website for the OS that you are currently working on (Windows/MacOS/Linux)
- ```Dockerfile.yaml``` contains all the instructions required to setup everything
- Following are the commands to setup the docker container
    ```
    docker build -t resume_scoring -f Dockerfile.yaml .
    docker run -it resume_scoring:latest bash
    ```
- Copy the ```sample/resume, Job_Description.txt, skills.csv``` files from the host pc to the docker container using ```docker cp <SOURCE_DIR> resume_scoring:/home/Resume_Parser/```

_Note: This is currently a prototype which requires a lot of human intervention. This can easily be used as a web app to streamline all the inputs and outputs in a proper definitive way. Due to less time, I couldn't work on it so if anyone is willing to create a pull request and collaborate on this I'll be more than happy to work on it_

**_If you have any issues, please feel free to create a pull request or reach out to me at thakkar.dhaval.haresh@gmail.com_**

## License
MIT
**Free Software, Hell Yeah!**
