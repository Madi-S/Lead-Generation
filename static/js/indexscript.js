let autocomplete;

function showRecomendations() {
  // Initialize the autocomplete functionality
  const input = document.getElementById("location");
  console.log(input);
  autocomplete = new google.maps.places.Autocomplete(input);

  autocomplete.addListener("place_changed", () => {
    const place = autocomplete.getPlace();
    if (!place.geometry || !place.geometry.location) {
      window.alert("No details available for input: '" + place.name + "'");
      return;
    }
  });
}

// Initialize the map and Autocomplete when the window loads
window.onload = showRecomendations;

/* let map;
let autocomplete;
let infowindow;
let infowindowContent;

async function initMap() {
// Initialize the map centered around a default location
const defaultLocation = {
  lat: 32.82400144764479,
  lng: 73.84835279577405,
}; // Sydney, Australia
map = new google.maps.Map(document.getElementById("map"), {
  center: defaultLocation,
  zoom: 13,
});

infowindow = new google.maps.InfoWindow();
console.log(infowindow);
infowindowContent = document.createElement("div");
infowindow.setContent(infowindowContent);

// Initialize the autocomplete functionality
const input = document.getElementById("location-input");
autocomplete = new google.maps.places.Autocomplete(input);
autocomplete.bindTo("bounds", map);

autocomplete.addListener("place_changed", () => {
  infowindow.close();
  const place = autocomplete.getPlace();

  if (!place.geometry || !place.geometry.location) {
    window.alert(
      "No details available for input: '" + place.name + "'"
    );
    return;
  }

  if (place.geometry.viewport) {
    map.fitBounds(place.geometry.viewport);
  } else {
    map.setCenter(place.geometry.location);
    map.setZoom(17);
  }

  const marker = new google.maps.Marker({
    position: place.geometry.location,
    map: map,
  });

  infowindowContent.textContent =  place.name + "\n" + place.formatted_address;
  infowindow.open(map, marker);
});
console.log(infowindowContent.textContent);
}*/
