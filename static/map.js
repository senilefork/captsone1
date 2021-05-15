let map;
let markers = []
let coordinatesArray = []

//when window loads get apartments array from getApartments and pass it to initMap
//this gets all apartments from our api and puts them on the map
window.onload = async function(){
  coordinatesArray = await getApartments()
  initMap(coordinatesArray)
  coordinatesArray = []
}

//get all apartments from our api and return them in an array with coordinates, street and price
async function getApartments(){
  let res = await axios.get('http://127.0.0.1:5000/get_apartments_json')
  let apartments = res.data.apartments
  for(let i = 0; i < apartments.length; i++){
    coordinatesArray.push([apartments[i]["coordinates"], apartments[i]["street"], apartments[i]["price"]])
  } 
  return coordinatesArray
}

//initiate a new map with google maps api and put brooklyn at the center
//initMap then takes an array and creates and puts a new marker on the map
function initMap(array) {
  //new map with options
map = new google.maps.Map(document.getElementById("map"), {
  center: { lat: 40.683347, lng: -73.953903 },
  zoom: 12,
});

for(let i = 0; i < array.length; i++){
  addMarker(array[i])
  }
}

//filter form allows us to filter through apartments with a given criteria
let filterForm = document.getElementById("filter-apartment-form")
filterForm.addEventListener("submit", async function(e){
  e.preventDefault()
//first delete all markers off the current map
  deleteMarkers(markers)

//create some variables that we will use to contruct our apartment object to be passed as
//a param in our axios call that we will make after collecting form data
  let valueArray = []
  let keyArray = ["price", "management_id", "street", "city", "beds", "baths", "laundry", "backyard", "balcony", "rooftop_access", "neighborhood", "availability"]
  let filterObject = {}

//collect form data and push given value onto our valueArray
  let price = document.getElementById("price").value 
  valueArray.push(price)
  let management = document.getElementById("management").value
  valueArray.push(management)
  let street = document.getElementById("street").value
  valueArray.push(street)
  let city = document.getElementById("city").value 
  valueArray.push(city)
  let beds = document.getElementById("beds").value 
  valueArray.push(beds)
  let baths = document.getElementById("baths").value
  valueArray.push(baths) 
  let laundry = document.getElementsByName("laundry")
  let laundryValue = getRadioValue(laundry)
  valueArray.push(laundryValue)
  let backyard = document.getElementsByName("backyard")
  let backyardValue = getRadioValue(backyard)
  valueArray.push(backyardValue)
  let balcony = document.getElementsByName("balcony")
  let balconyValue = getRadioValue(balcony)
  valueArray.push(balconyValue)
  let rooftop_access = document.getElementsByName("rooftop_access")
  let rooftop_accessValue = getRadioValue(rooftop_access)
  valueArray.push(rooftop_accessValue)
  let neighborhood = document.getElementById("neighborhood").value 
  valueArray.push(neighborhood)
  let availability = document.getElementById("availability").value 
  valueArray.push(availability)

//iterate through our valueArray and if a value isn't 0 or "" create a key value pair
//on our filterObject using keyArray values as key and ValuesArray values as values 
  for(let i = 0; i < valueArray.length; i++){
    if(valueArray[i] != "" && valueArray[i] != 0){
      let keys = keyArray[i]
      let values = valueArray[i]
      filterObject[keys] = values
    }
  }
//pass our filerObject to /filter_apartments endpoint to recieve filtered apartments json
  res = await axios.get('http://127.0.0.1:5000/filter_apartments', { params: filterObject})
  let filteredApartments = res.data.apartments

//iterate over our filtered apartments extracting the data that we want
  for(let i = 0; i < filteredApartments.length; i++){
    coordinatesArray.push([filteredApartments[i]["coordinates"], filteredApartments[i]["street"], filteredApartments[i]["price"]])
  } 
//pass our data to initMap and empty array for next call
  initMap(coordinatesArray)
  coordinatesArray = []
  console.log(markers)
})

//addMarker is a function that makes use of the Marker and InfoWindow classes provided by the 
//google maps api. addMarker takes and array, assuming that the array provides coordinates, street and price
//it then puts a new Marker on our map and also provides an infoWindow
function addMarker(location){
  let marker = new google.maps.Marker({
    position : location[0],
    map : map
  })
  const infowindow = new google.maps.InfoWindow({
    content: `${location[1]}, $${location[2]}`
  });
  marker.addListener("click", () => {
    infowindow.open(map, marker);
  });
  markers.push(marker)
}



//deleteMarkers function and deletes them by setting their map to null, then empty markers array for next call
function deleteMarkers(array){
  for(let i = 0; i < array.length; i++){
    array[i].setMap(null)
  }
  markers= []
}

//function for getting input value of a radio field
function getRadioValue(ul){
  for (let i = 0; i < ul.length; i++){
    if(ul[i].checked){
      return ul[i].value
    }
  }
  return ""
}