# Project Description:

This project demonstrates Infrastructure as Code (IaC) principles, using the Serverless Framework to deploy a scalable and cost-efficient serverless application. The app provides functionalities to list ads, create, modify, and delete ads, and incorporates a real-time chat feature for each ad, enabling users to engage in discussions or comments related to each item.

The architecture is built on AWS Lambda, API Gateway, and DynamoDB, ensuring low operational costs through AWS's pay-per-use model. The chat functionality is based on code adapted from this repository, adding dynamic user interaction while maintaining serverless efficiency.

The project benefits from IaC, enabling rapid deployment and infrastructure replication, reducing manual errors, and speeding up development cycles. A Bash script automates the entire deployment, from setting up the infrastructure to populating the DynamoDB database with test data and launching the application in the browser.

From an operational standpoint, this architecture allows the application to scale effortlessly while keeping costs minimal. AWS Lambda charges are based only on the actual compute time used, and DynamoDB only incurs costs during active usage, making it ideal for small to medium applications with fluctuating demands.
