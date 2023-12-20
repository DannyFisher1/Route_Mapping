function initMap() {
    const directionsService = new google.maps.DirectionsService();
    const base = {lat: 38.8033, lng: -76.8719};  // Joint Base Andrews

    {% for name in hospitals %}
    const map_{{ loop.index }} = new google.maps.Map(document.getElementById('map_{{ loop.index }}'), {
        zoom: 12,
        center: base
    });
    const directionsDisplay_{{ loop.index }} = new google.maps.DirectionsRenderer();
    directionsDisplay_{{ loop.index }}.setMap(map_{{ loop.index }});

    directionsService.route({
        origin: base,
        destination: base,
        travelMode: 'DRIVING',
        waypoints: [{location: "{{ name }}", stopover: true}],
        optimizeWaypoints: true,
    }, function(response, status) {
        if (status === 'OK') {
            directionsDisplay_{{ loop.index }}.setDirections(response);
            const outboundLeg = response.routes[0].legs[0];
            const returnLeg = response.routes[0].legs[1];
            const totalDuration = outboundLeg.duration.value + returnLeg.duration.value;
            const totalDurationText = Math.floor(totalDuration / 60) + " mins";
            document.getElementById('time_{{ loop.index }}').textContent = "Total travel time: " + totalDurationText;
        } else {
            console.error('Directions request failed due to ' + status);
        }
    });
    {% endfor %}
}