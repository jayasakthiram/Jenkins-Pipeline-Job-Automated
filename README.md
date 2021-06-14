# Automated Jenkins Pipeline Job
This resource will help in creating jenkins jobs automatically using python script.

## Note
- This demo module creates Jenkins Pipeline Job
- Pipeline job is created using scm mode, where a JenkinsFile is present in scm repo, here we use Git.
- You can have git repo even with sub folders, and it can be handled using sparse checkout technique.
## Workflow Diagram
![Design View](https://github.com/mynameisjai/Automated_Jenkins_Jobs/blob/main/automated_jenkins_job.png?raw=true)


### Python libraries used
- **requests** <br>
Requests library for accessing jenkins rest api.
- **warnings** <br>
To supress warning message from console log output using warnings library. <p>
- >pip install lxml
- **xml** <br>
Creating a xml config file using Etree library.

---
- Author : Jayasakthiram N <br>
- Input File: automate_jobs.py <br>
- Date Modified: 14th June 2021 
---