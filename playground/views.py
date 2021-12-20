from django.shortcuts import render
from django.http import HttpResponse
from SPARQLWrapper import SPARQLWrapper, RDFXML
from SPARQLWrapper.Wrapper import JSON
from rdflib import Graph
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
#request-handler

def generateArtworks(floornumber):
    sparql = SPARQLWrapper("http://ec2-3-142-213-172.us-east-2.compute.amazonaws.com:3030/ArtistDataSet/query")

    sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX ds: <http://purl.org/ctic/dcat#>
    PREFIX art: <http://w3id.org/art/terms/1.0/>
    PREFIX awssource1: <http://ec2-34-214-181-244.us-west-2.compute.amazonaws.com:3030/LocationDataSet/>
    PREFIX awssource2: <http://ec2-54-86-100-20.compute-1.amazonaws.com:3030/ArtworkDataSet/>
    PREFIX awssource3: <http://ec2-3-142-213-172.us-east-2.compute.amazonaws.com:3030/ArtistDataSet/>


    PREFIX artist:<http://www.semanticweb.org/bakthasrikanth/ontologies/2021/10/sam-artist#>
    PREFIX artwork:<http://www.semanticweb.org/baktha/ontologies/2021/10/SAAM_Artwork#>
    PREFIX location:<http://www.semanticweb.org/bakthasrikanth/ontologies/2021/10/location#>
                
    SELECT DISTINCT ?artworkImage ?locationID ?width ?title ?artistID
    WHERE {
    SERVICE awssource1:sparql {
    ?location location:hasLocationID ?locationID.
        FILTER (?locationID = """ + '"'+ str(floornumber) +'"'+ """)
    }
    SERVICE awssource2:sparql {
    ?artwork artwork:hasLocationID ?locationID.
    ?artwork artwork:hasWidth ?width.
    ?artwork artwork:hasTitle ?title.
    ?artwork artwork:hasArtistID ?artistID.
    ?artwork artwork:hasURLofImage ?artworkImage.
    ?artwork artwork:hasLocationID ?locationID2.
    FILTER (?locationID2 = ?locationID)
    }
    }
    Limit 10
    """)


    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()

    results=result['results']['bindings']
    artworkImages=list()
    artworkWidth=list()
    artworkTitle=list()
    artistsOfImages=list()
    


    for i in results:
        try:
            artworkImages.append(i['artworkImage']['value'])
        except:
            artworkImages.append("Unavailable")
        try:
            artworkWidth.append(i['width']['value'])
        except:
            artworkWidth.append("Unavailable")
        try:
            artworkTitle.append(i['title']['value'])
        except:
            artworkTitle.append("Unavailable")
        try:
            artistsOfImages.append(i['artistID']['value'])
        except:
            artistsOfImages.append("Unavailable")
        
            
            
    artistFirstName=list()
    artistLastName=list()
    artistPublicCaption=list()
    artistImage=list()
    for i in artistsOfImages:
        sparql.setQuery( """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX ds: <http://purl.org/ctic/dcat#>
        PREFIX art: <http://w3id.org/art/terms/1.0/>
        PREFIX awssource1: <http://ec2-34-214-181-244.us-west-2.compute.amazonaws.com:3030/LocationDataSet/>
        PREFIX awssource2: <http://ec2-54-86-100-20.compute-1.amazonaws.com:3030/ArtworkDataSet/>
        PREFIX awssource3: <http://ec2-3-142-213-172.us-east-2.compute.amazonaws.com:3030/ArtistDataSet/>
        PREFIX artist:<http://www.semanticweb.org/bakthasrikanth/ontologies/2021/10/sam-artist#>
        PREFIX artwork:<http://www.semanticweb.org/baktha/ontologies/2021/10/SAAM_Artwork#>
        PREFIX location:<http://www.semanticweb.org/bakthasrikanth/ontologies/2021/10/location#>

        SELECT DISTINCT ?FirstName ?LastName ?publicCaption ?artistImage
        WHERE {
        SERVICE awssource3:sparql {
        ?artist artist:hasFirstName ?FirstName.
        ?artist artist:hasLastname ?LastName.
        ?artist artist:hasPubliccaption ?publicCaption.  
        ?artist artist:hasImgURL ?artistImage. 
        ?artist artist:hasArtistID ?artistID2.
        FILTER (?artistID2 =""" + '"'+ i +'"'+ """)
        }
        }
        """)

        sparql.setReturnFormat(JSON)
        result = sparql.query().convert()

        results=result['results']['bindings']

        try:
            artistFirstName.append(results[0]['FirstName']['value'])
        except:
            artistFirstName.append("Unavailable")
        try:
            artistLastName.append(results[0]['LastName']['value'])
        except:
            artistLastName.append("Unavailable")
        try:
            artistPublicCaption.append(results[0]['publicCaption']['value'])
        except:
            artistPublicCaption.append("Unavailable")
        try:
            artistImage.append(results[0]['artistImage']['value'])
        except:
            artistImage.append("Unavailable")

   
    return artworkImages, artworkWidth, artworkTitle, artistFirstName, artistLastName, artistPublicCaption, artistImage

def searchArtwork(keystring):
    sparql = SPARQLWrapper("http://ec2-3-142-213-172.us-east-2.compute.amazonaws.com:3030/ArtistDataSet/query")

    sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX ds: <http://purl.org/ctic/dcat#>
    PREFIX art: <http://w3id.org/art/terms/1.0/>
    PREFIX awssource1: <http://ec2-34-214-181-244.us-west-2.compute.amazonaws.com:3030/LocationDataSet/>
    PREFIX awssource2: <http://ec2-54-86-100-20.compute-1.amazonaws.com:3030/ArtworkDataSet/>
    PREFIX awssource3: <http://ec2-3-142-213-172.us-east-2.compute.amazonaws.com:3030/ArtistDataSet/>


    PREFIX artist:<http://www.semanticweb.org/bakthasrikanth/ontologies/2021/10/sam-artist#>
    PREFIX artwork:<http://www.semanticweb.org/baktha/ontologies/2021/10/SAAM_Artwork#>
    PREFIX location:<http://www.semanticweb.org/bakthasrikanth/ontologies/2021/10/location#>
                
    SELECT DISTINCT ?artworkImage ?title ?width ?artistID
    WHERE {
    SERVICE awssource2:sparql {
    ?artwork artwork:hasLocationID ?locationID.
    ?artwork artwork:hasWidth ?width.
    ?artwork artwork:hasTitle ?title.
    ?artwork artwork:hasArtistID ?artistID.
    ?artwork artwork:hasURLofImage ?artworkImage.
    ?artwork artwork:hasLocationID ?locationID2.
    FILTER regex(?title,""" +'"'+keystring+'")'+ """
    }
    }
    Limit 5
    """)

    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()

    results=result['results']['bindings']

    artworkImage=[]
    artworkTitle=[]
    artworkWidth=[]
    artistId=[]

    for i in results:
        try:
            artworkImage.append(i['artworkImage']['value'])
            artworkTitle.append(i['title']['value'])
            artworkWidth.append(i['width']['value'])
            artistId.append(i['artistID']['value'])
        except:
            pass

    artistFirstName=list()
    artistLastName=list()
    artistPublicCaption=list()
    artistImage=list()

    for i in artistId:
        sparql.setQuery( """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX ds: <http://purl.org/ctic/dcat#>
        PREFIX art: <http://w3id.org/art/terms/1.0/>
        PREFIX awssource1: <http://ec2-34-214-181-244.us-west-2.compute.amazonaws.com:3030/LocationDataSet/>
        PREFIX awssource2: <http://ec2-54-86-100-20.compute-1.amazonaws.com:3030/ArtworkDataSet/>
        PREFIX awssource3: <http://ec2-3-142-213-172.us-east-2.compute.amazonaws.com:3030/ArtistDataSet/>
        PREFIX artist:<http://www.semanticweb.org/bakthasrikanth/ontologies/2021/10/sam-artist#>
        PREFIX artwork:<http://www.semanticweb.org/baktha/ontologies/2021/10/SAAM_Artwork#>
        PREFIX location:<http://www.semanticweb.org/bakthasrikanth/ontologies/2021/10/location#>

        SELECT DISTINCT ?FirstName ?LastName ?publicCaption ?artistImage
        WHERE {
        SERVICE awssource3:sparql {
        ?artist artist:hasFirstName ?FirstName.
        ?artist artist:hasLastname ?LastName.
        ?artist artist:hasPubliccaption ?publicCaption.  
        ?artist artist:hasImgURL ?artistImage. 
        ?artist artist:hasArtistID ?artistID2.
        FILTER (?artistID2 =""" + '"'+ i +'"'+ """)
        }
        }
        """)

        sparql.setReturnFormat(JSON)
        result = sparql.query().convert()

        results=result['results']['bindings']

        try:
            artistFirstName.append(results[0]['FirstName']['value'])
        except:
            artistFirstName.append("Unavailable")
        try:
            artistLastName.append(results[0]['LastName']['value'])
        except:
            artistLastName.append("Unavailable")
        try:
            artistPublicCaption.append(results[0]['publicCaption']['value'])
        except:
            artistPublicCaption.append("Unavailable")
        try:
            artistImage.append(results[0]['artistImage']['value'])
        except:
            artistImage.append("Unavailable")

   
    return artworkImage, artworkWidth, artworkTitle, artistFirstName, artistLastName, artistPublicCaption, artistImage

    

@csrf_exempt 
def say_hello(request):
    floornumber="3"
    if(request.method=='POST'):
        floornumber=request.POST['floor']
    artworkImages, artworkWidth, artworkTitle, artistFirstName, artistLastName, artistPublicCaption, artistImage =generateArtworks(floornumber)
    return render(request, 'hello.html', {'artworkImages':artworkImages,'artworkWidth':artworkWidth,'artworkTitle':artworkTitle,'artistFirstName':artistFirstName,'artistLastName':artistLastName,'artworkTitle':artworkTitle,'artistImage':artistImage, 'artistPublicCaption':artistPublicCaption,'floornumber':floornumber})

@csrf_exempt 
def searchByName(request):
    keyString=""
    if(request.method=='POST'):
        keyString=request.POST['fname']
    
    artworkImages, artworkWidth, artworkTitle, artistFirstName, artistLastName, artistPublicCaption, artistImage =searchArtwork(keyString)
    return render(request, 'searchByArtwork.html', {'artworkImages':artworkImages,'artworkWidth':artworkWidth,'artworkTitle':artworkTitle,'artistFirstName':artistFirstName,'artistLastName':artistLastName,'artworkTitle':artworkTitle,'artistImage':artistImage, 'artistPublicCaption':artistPublicCaption,'keystring':keyString})



def floor(request):
    return render(request, 'FloorSelection.html')