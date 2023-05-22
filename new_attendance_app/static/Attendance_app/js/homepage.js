//  ----------------------------------for map-------------------------------------------

 // Define the endpoint for the API that returns the site data from the MySQL database
 const endpoint = 'http://127.0.0.1:8000/gate_config/site_data/';

 // Initialize the Google Maps map
 let map;
     let markers = []; // Array to store the markers
     let infoWindow; // Info window to show site information
     function initMap() {
       map = new google.maps.Map(document.getElementById('map'), {
         zoom: 6,
         center: { lat: 13.7749, lng: 77.4194 } // San Francisco
       });
 
       infoWindow = new google.maps.InfoWindow(); // Initialize the info window
 
       // Fetch the site data from the API and show markers on the map
       fetchSiteData();
 
       // Fetch site data every 30 seconds and update markers
       setInterval(fetchSiteData, 30000);
     }
 
     function fetchSiteData() {
       fetch(endpoint)
         .then(response => response.json())
         .then(data => {
           var tbl=" <tr><th>Site Name</th><th>Site ID</th>";
           document.getElementById('mytbl').innerHTML=tbl
           for(let i in data ){
            tbl += '<tr><td>'+data[i]["sitename"]+'</td><td>'+data[i]["siteid"]+'</td></tr>'
             console.log(data[i])
           // for(let j in data[i]){
           //   tbl +='<td>'+data[i][j]+'</td>'
           //   console.log(data[i][j])
           // }
           // tbl += '</tr>'
           }
           document.getElementById('mytbl').innerHTML=tbl
           // Remove existing markers from the map
           markers.forEach(marker => marker.setMap(null));
           markers = [];
 
           // Add markers for each site
           data.forEach(site => {
             const icon = site.enable
               ? 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
               : 'http://maps.google.com/mapfiles/ms/icons/red-dot.png';
 
             const marker = new google.maps.Marker({
               position: { lat: site.lat, lng: site.lng },
               map: map,
               title: site.sitename,
               icon: icon
             });
 
             // Add event listener to show site information when marker is clicked
             marker.addListener('click', () => {
               infoWindow.setContent(`
                 <div>
                   <h2>${site.sitename}</h2>
                   <p>Site ID: ${site.siteid}</p>
                   <p>Latitude: ${site.lat}</p>
                   <p>Longitude: ${site.lng}</p>
                 </div>
               `);
               infoWindow.open(map, marker);
             });
 
             markers.push(marker);
           });
         })
         .catch(error => console.error(error));
     }
