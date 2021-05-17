let apartmentsArray = []

//when home page loads get apartments info from api and pass data to addApartmentsToPage
window.onload = async function(){
    apartmentsArray = await getHomepageApartments()
    addApartmentsToPage(apartmentsArray)
    apartmentsArray = []
  }

  //get apartments json from api and return it in an array
  async function getHomepageApartments(){
    let res = await axios.get('https://capstone1-anna-f.herokuapp.com/get_apartments_json')
    let apartments = res.data.apartments
    for(let i = 0; i < apartments.length; i++){
      apartmentsArray.push(apartments[i])
    } 
    return apartmentsArray
  }

  //collect form data for filtering
  let homeForm = document.getElementById('home-filter-apartment-form')
  homeForm.addEventListener("submit", async function getFilteredApartments(e){
    e.preventDefault()
    
  let valueArray = []
  let keyArray = ["price", "management_id", "street", "city", "beds", "baths", "laundry", "backyard", "balcony", "rooftop_access", "neighborhood","availability"]
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
  let availability = document.getElementById("availability").value 
  valueArray.push(availability)
  
//this logic works the same as map.js file
  for(let i = 0; i < valueArray.length; i++){
    if(valueArray[i] != "" && valueArray[i] != 0){
      let keys = keyArray[i]
      let values = valueArray[i]
      filterObject[keys] = values
    }
  }

  //get filtered apartments json, add to array and pass array to addApartmentsToPage function
  res = await axios.get('https://capstone1-anna-f.herokuapp.com/filter_apartments', { params: filterObject})
  apartmentsArray = res.data.apartments
  addApartmentsToPage(apartmentsArray)
  })

  //this function takes an array of apartment objects and adds html with individual apartment data
  function addApartmentsToPage(arrayOfObjects){
    let homepageListDiv = document.querySelector('.home_page_list');

    while(homepageListDiv.firstChild){
      homepageListDiv.removeChild(homepageListDiv.firstChild)
    }

    for(let i = 0; i < arrayOfObjects.length; i++){
        let apartment = arrayOfObjects[i]
        let pTag = document.createElement('p')
        pTag.className = "list-apt"
        //create management p tag
        let managementP  = document.createElement('p')
        managementP.innerHTML = apartment.management_name
        pTag.append(managementP)
        //create street p tag with nested a tag
        let streetPTag = document.createElement('p')
        let streetATag = document.createElement('a')
        streetATag.setAttribute('href', `/detail/${apartment.id}`)
        streetATag.innerHTML = `${apartment.street} apt# ${apartment.apartment_number}`
        streetPTag.append(streetATag)
        pTag.append(streetPTag)
        //create area p tag
        let areaP = document.createElement('p')
        areaP.innerHTML = `${apartment.neighborhood} ${apartment.city}`
        pTag.append(areaP)
        //create price p tag
        let priceP = document.createElement('p')
        priceP.innerHTML = `$${apartment.price}`
        pTag.append(priceP)
        homepageListDiv.append(pTag)
        //create edit p tag
        let editPTag = document.createElement('p')
        let editATag = document.createElement('a')
        editATag.setAttribute('href', `/edit_apartment/${apartment.id}`)
        editATag.innerHTML = 'edit'
        editPTag.append(editATag)
        pTag.append(editPTag)
        //create delete p tag
        let deletePTag = document.createElement('p')
        let deleteATag = document.createElement('a')
        deleteATag.setAttribute('href', `/delete/${apartment.id}`)
        deleteATag.innerHTML = 'delete'
        deletePTag.append(deleteATag)
        pTag.append(deletePTag)
    }
  }

//get value of radio field
  function getRadioValue(ul){
    for (let i = 0; i < ul.length; i++){
      if(ul[i].checked){
        return ul[i].value
      }
    }
    return ""
  }