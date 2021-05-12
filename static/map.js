let map;
let markers = []
let coordinatesArray = []

window.onload = async function(){
  coordinatesArray = await getApartments()
  initMap(coordinatesArray)
  coordinatesArray = []
}

async function getApartments(){
  let res = await axios.get('http://127.0.0.1:5000/get_apartments_json')
  let apartments = res.data.apartments
  for(let i = 0; i < apartments.length; i++){
    coordinatesArray.push(apartments[i]["coordinates"])
  } 
  //console.log(apartments)
  //console.log(coordinatesArray)
  return coordinatesArray
}

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

let filterForm = document.getElementById("filter-apartment-form")
filterForm.addEventListener("submit", async function(e){
  e.preventDefault()
  deleteMarkers(markers)

  let valueArray = []
  let keyArray = ["price", "management_id", "street", "city", "beds", "baths", "laundry", "backyard", "balcony", "rooftop_access", "neighborhood"]
  let filterObject = {}

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
  console.log(valueArray)
  
  for(let i = 0; i < valueArray.length; i++){
    if(valueArray[i] != "" && valueArray[i] != 0){
      let keys = keyArray[i]
      let values = valueArray[i]
      filterObject[keys] = values
    }
  }
  console.log(filterObject)
  res = await axios.get('http://127.0.0.1:5000/filter_apartments', { params: filterObject})
  let filteredApartments = res.data.apartments
 
  for(let i = 0; i < filteredApartments.length; i++){
    coordinatesArray.push(filteredApartments[i]["coordinates"])
  } 
  initMap(coordinatesArray)
  coordinatesArray = []
  //console.log(markers)
})

function addMarker(location){
  let marker = new google.maps.Marker({
    position : location,
    map : map
  })
  markers.push(marker)
}


function deleteMarkers(array){
  for(let i = 0; i < array.length; i++){
    array[i].setMap(null)
  }
  markers= []
}

function getRadioValue(ul){
  for (let i = 0; i < ul.length; i++){
    if(ul[i].checked){
      return ul[i].value
    }
  }
  return ""
}