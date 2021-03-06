# ECS260-project

<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#data-restoration">Data Restoration</a></li>
        <li><a href="#data-filtering">Data Filtering</a></li>
        <li><a href="#preliminary-data-analysis">Preliminary Data Analysis</a></li>
      </ul>
    </li>
    <li><a href="#Contributors">Contributors</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

The is a code and data repository associated with the research of Team 6 in ECS260. The topic of our research is <em>An Empirical Study of Tests in Open-source Projects of TravisCI on GitHub </em>.

<!-- GETTING STARTED -->
### Data Restoration
We download and restore MySQL dump files (http://ghtorrent-downloads.ewi.tudelft.nl/mysql/mysql-2021-03-06.tar.gz) from GHTorrent into a MySQL database on virtual machines running on Google Cloud Platform (GCP)

We selected the most popular repositories (more than or equals to 494 stars) by running the following SQL in the restored database:
```SQL
select u.login, p.name, p.language, count(*)
from projects p, users u, watchers w
where
    p.forked_from is null and
    p.deleted is false and
    w.repo_id = p.id and
    u.id = p.owner_id
group by p.id
having count(*) >= 494
order by count(*) desc
```

### Data filtering
We found that TravisPoker,  the tool included in TravisTorrent project (https://github.com/TestRoots/travistorrent-tools) for checking if a repository use Travis CI, is unusable possibly due to lack of maintenance. Therefore we studied TravisTorrent source code and developed our own Node.js program that queries Travis API to check the usage of Travis CI in all of the repositories indicated by the rows in .csv file. 

To use this program, the developer should have Node.js installed on the machine and run the following command in the project directory:
```console
npm install
node index.js
```
This will produce 'repos_2021_500_out.csv' file, which an integer at the end of each row indicating the 'last_build_number'. If the number is -1, then it means the repo does not use Travis CI.

### Preliminary Data Analysis
We developed Python program to do preliminary data analysis based on 'repos_2021_500_out.csv' file to find differences in the use of Travis CI in different language projects, and visualize the results.

![Preliminary Data Analysis Result](/travis_ci_repos_2021_500_out.png)

## Contributors
Haochen Yang, Haoming Sun, Siyuan Liu, Yuxuan Chen, Zhengyang Jia
