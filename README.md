# Retrospective 
Retrospective app to conduct Retrospective meetings online (Agile methodology).  
App has objects:
* Retro
* Cards
* Teams

GraphQL API
-------------------------------------------------------
List of URLs:
- /graphql/ POST requests on GraphQL API
- /schema/ Returns json schema for Apollo

In Browser you can send  requests to graphql api
Examples of requests:
```graphql
{  
  allUsers  
  {  
    edges
        {  
          node  
              {  
                id  
                email  
                lastName  
                firstName        
              }  
        } 
  }  
}  
```

## Installation (For Linux):

* git clone https://github.com/antl31/retrospective_app
* cd retrospective_app/
* sudo docker-compose build 
* sudo docker-compose up
* docker exec -it web sh  
in container:
  *  python3 manage.py migrate
  * python3 manage.py collectstatic