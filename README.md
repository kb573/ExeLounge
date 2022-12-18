# ExeLounge

This is ExeLounge, a web app developed for ECM2434 by Group I.

ExeLounge is a web app built on Django that allows students to easily interact with other students in their department,
course, and even in the same modules. It has a leaderboard based on interactions with the forum that encourages students
to participate by asking and answering each other's questions.

You can access the deployed app here: [https://exelounge.herokuapp.com/](https://exelounge.herokuapp.com/)

## Fulfilling the [Principles of Software Engineering](https://vle.exeter.ac.uk/pluginfile.php/2431244/mod_label/intro/SEGP1.1-software-engineering-principles.pdf#page=6)

### Testability

We've built-in unit tests to ensure that individual blocks of code perform accurately and as expected.

Once we've completed the MVP and our product is nearing completion, we'd like to test it with a variety of students, to
get real user feedback. Testing it with students throughout the development process is important to ensure that the
direction we take our product in is shaped by user feedback.

### Maintainability

We've added comments and docstrings throughout our code, to ensure that other developers can understand our work. We've
also taken care to follow naming conventions (e.g. for variables), and have chosen names that are concise, consistent,
and easy to understand.

Our database uses PostgreSQL and is cloud-based, so it can be accessed from anywhere.

### Integrity

Our database is based in the cloud and not on-site at the University, which means there isn't a single point of failure.
Regular and automatic backups are enabled by default in IBM Cloud, allowing the database to be restored to a known good
state in the event of failure.

IBM Cloud employs
a wide variety of methods to protect data
within the database, including LUKS with AES-256 encryption for stored data and TLS/SSL encryption for data in transit.
It also conforms to the applicable guidelines for information security defined
in [ISO 27017](https://www.iso.org/standard/43757.html) and [ISO 27018](https://www.iso.org/standard/76559.html). They have further, extensive details on the security of their dataabase platform here: https://cloud.ibm.com/docs/databases-for-postgresql?topic=databases-for-postgresql-security-compliance

The hosting of our app on Heroku is also secure. The connection to the site is encrypted and authenticated using TLS 1.2, ECDHE_RSA with P-256, and AES_128_GCM. Heroku uses ISO 27001 and FISMA certified data centers managed by Amazon. Each application on their platform runs within its own isolated environment, so they cannot interact with other applications or areas of the system. They have further, extensive details on the security of their platform here: https://www.heroku.com/policy/security

### External integration is well-defined

In the ideal world, we'd want to integrate our app with the University Single Sign-On (SSO) and the Student Records
System (SRS).

- Integration with SSO would mean that the student wouldn't need to create a new account and could log-in with the same
  account that they use for all other services provided by the University.
- Integration with SRS would mean that the student wouldn't need to enter their personal and course details, these could
  instead be pulled directly from the University.
- Combined, these would enable students to use our app easily and efficiently by simply signing in with their University
  credentials, and relying on the data stored by the University.
- Accessing data that the University already stores would mean that an extra copy of it doesn't need to be stored by us,
  which would prevent inconsistencies arising and remove our burden of storing the personal data securely in line with
  the [Data Protection Act 2018](https://www.legislation.gov.uk/ukpga/2018/12/contents).

After the initial testing [described above](#testability), we would want to initially roll out the app within a single
department before expanding to the rest of the department's college, to other colleges, and finally the whole
institution.

- This rollout could start in the Computer Science department in CEMPS because they are expected to be the most
  tech-savvy students, and may be able to provide precise, technical feedback.
- However, it might be appropriate to start with another department that isn't expected to be the most tech-savvy (such
  as in CHUMS) because our app must be accessible to and easy to use by everyone.
- Feedback gathered during the rollout would continue to help refine the final product.

### Ethics

We've designed our product to only collected the data required for it to function. As a result, we don't collect
addresses nor phone numbers, because the app has no functionality that depends on this data.

The data is stored securely on IBM Cloud (as [described above](#integrity)) and is only accessible to the project team
and the module convenor. It would only be shared with the required University staff and would not be shared with third
parties.

Our app has a leaderboard, however by default students are not visible on the leaderboard, and are free to choose to
what extent they are visible on it (either not at all, with just their initials, with just their first name, or with
their full name).

Students also have the option to interact anonymously with each other on the forums. These interactions are anonymous to
their peers however designated staff are still able to identify the authors of forum posts and replies to discourage and
track inappropriate content.

### Management

We've followed the Kanban Agile Methodology, and have used
a [Trello board](https://trello.com/b/k7vwZUVa/the-kanban-board) to manage our project. Where possible, we've also
worked to ensure that specification, implementation, and validation of tasks are each completed by different team
members, to help catch any errors and ensure that everyone has a good understanding of the entire project. We've also used feature branches to allow different components to be worked on simultaneously, and pull requests to help facilitate validation.

We hold short, regular meetings every 2 to 3 days to discuss the project's progress, prioritise tasks, and discuss any
setbacks that we're encountering. 

In the ideal world, we'd also want to have regular meetings with key stakeholders (such as academics and senior
management) to discuss what they want the project to achieve, and what direction they'd like us to take it in. It could
also be useful to hold focus group sessions with students to get valuable student feedback on potential ideas.
