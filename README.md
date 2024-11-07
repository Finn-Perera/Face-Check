<h1>Face Check</h1>
<h4>Project Started: 12/08/2024</h4>

  **Face Check** is a web application aimed at comparing the prices of skincare products across different websites,
  finding the best prices for any given item. **It is a personal project and does not intend to make any monetary gain.**
  It is yet to be hosted, although I would like to host it in the future.

<h3> Motivation </h3>
  I began the project understanding that over many web stores, some will have differing prices on their products.
  As such there are ways for people to benefit from having a centralised location to find all of those prices for their
  wishlist of products.
<br></br>

  I then wanted to find ways to filter and browse these products, all the while slowly coming to the realisation it had all
  been done far better by a large organisation! Which was disheartening but still would not stop me learning from the development
  process.
<h3> What I learned </h3>

  While I had made much smaller web pages in the past, getting to learn basic **HTML**, **CSS**, and **JavaScript**, I had never tried a full
  web application. After learning the basics of **Java Springboot** at University, I decided to create a backend consisting of **MariaDB SQL**
  and **Java** as a REST api to retrieve data from.
 <br></br>
  The method of gathering data was utilising **Web Scraping**, which I had never done but had heard of.
  I found the **Selenium** library in **Python** to work well for gathering the information from websites, in the meantime learning
  the legalities of such a process, reading the robot.txt files of websites I scraped, I would not profit from this at all and would not expose
  any delicate information. The front end I chose to keep simple and learn the roots instead of employing a framework,
  so I went with pure **HTML** **CSS** and **JS**.
  <br></br>
   
  <h4>The skills I learned:</h4>
  <ul>
    <li><b>SQL</b></li>
    <li><b>HTML</b></li>
    <li><b>CSS</b></li>
    <li><b>JavaScript</b></li>
    <li><b>Java Springboot</b></li>
    <li><b>Python (Selenium & MySQL Connector)</b></li>
  </ul>

<h3> What would I do better </h3>

The worst problem I faced was the **lack of flexability a purely SQL based database was**. When I started the project I hadn't
thought too much about the structure of the database I was going to implement, and as such I was constantly needing to update and
change the schema, introduce relationships and data. This was problematic and caused progress to be extremely slow, especially since
my webscraping scripts were tailor made to the schema. Any additional feature I wanted to introduce required adjusting each webscraping
script, database table/schema, springboot API, and JavaScript that fetched information from the api.
<br></br>
To redo this I would instead begin by extensively planning the features of the application, understanding what data would be required
for said features. Then I would use **PostgreSQL** or a framework that can produce a better schema, like **Laravel** (Which I am currently learning).
<br></br>
Another issue I faced was the individuality of websites when webscraping, to set a webscraper up it would require lots of tinkering
as each website's css and html was vastly different. It would often take a few hours to create a robust scraper. If I were to remake the project
I would find a more modular way to handle webscraping, to make it much less time consuming to set up any new ones. I attempted this with
the connector script, which took in the lists of items from scrapers and sent the valid items to the database to be stored.
<br></br>
<h3> What next for Face Check? </h3>

In continuing this project I would like to achieve:
 <br></br>
<ul>
  <li><b>Hosting through a cloud service</b></li>
  <li><b>Additional websites scraped for more options</b></li>
  <li><b>A better rating system</b></li>
  <li><b>An ingredients list from each item</b></li>
  <li><b>A breakdown of pros and cons of ingredients</b></li>
  <li><b>Keeping track of different sizes of the same product</b></li>
</ul>
 <br></br>
Even if it doesn't reach all of these objectives, this project was a positive step for my understanding of web development
and really helped me learn about how to go about programming a web application. 

