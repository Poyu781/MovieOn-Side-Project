# [MovieOn](https://movieon.tw/)

**A movie introduction website which enables search for rating data, with the integration of IMDb,  RottenTomatoes, and Douban**

![](https://i.imgur.com/INyMEWn.jpg)



### Website : https://movieon.tw

#### Test Account

* Account: test_account
* Password: trymypage

Login to test the user-only function (Rating, Collection and Similarity Report)

## Table of Contents
* [Data Pipeline](#Data-Pipeline)
* [MySQL Schema](#MySQL-Schema)
* [Server Structure](#Server-Structure)
* [Features](#Features)
* [Technologies](#Technologies)






## Data Pipeline
![](https://i.imgur.com/Kwjc2Cy.png)


### Airflow Flowchart

#### **Movie Data Extract Transform Dag** 
![](https://i.imgur.com/6wPQQTH.png)

---
#### **Movie Data Load Dag** 
![](https://i.imgur.com/3wOrXKD.png)



## MySQL Schema
For better resolution, please click [here](https://stylishforjimmy.s3.ap-northeast-1.amazonaws.com/Untitled.png)
![](https://i.imgur.com/NMKjN4d.png)



## Server Structure

![](https://i.imgur.com/rNtwusQ.png)


## Features
### Data pipeline dashboard
![](https://i.imgur.com/MPDDWOk.gif)
### Search movies with multiple conditions
![](https://i.imgur.com/5hOj2nK.gif)
### Search movies by title
![](https://i.imgur.com/juKxucJ.gif)
### Show movie page with recommended movies
![](https://i.imgur.com/aJho2zh.gif)
### Show member page with similarity report
![](https://i.imgur.com/r1moJVY.gif)



## Technologies
> Data Pipeline
* Airflow

> Backend
* Django

> Database
* MongoDB
* MySQL
* Redis

> Frontend
* HTML
* CSS
* JavaScript

> Networking
* Nginx
* SSL Certificate(**Let's Encrypt**)

> Others
* AWS EC2
* AWS RDS
* AWS S3
* Google Search API

## Contact Me

Poyu Chiu  poyu.qiu@gmail.com