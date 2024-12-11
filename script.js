document.addEventListener('DOMContentLoaded', function() {
    // Initialize the map centered on downtown LA
    const map = L.map('map').setView([34.0522, -118.2437], 14); // Downtown LA coordinates

    // Add a dark theme map layer
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '©OpenStreetMap, ©CartoDB',
        maxZoom: 19
    }).addTo(map);

    // Simulate crowd density data for different LA locations
    const heatData = [
        // LA Live / Crypto.com Arena area (high density)
        [34.0430, -118.2673, 0.9],
        [34.0431, -118.2671, 0.8],
        [34.0432, -118.2670, 0.9],
        [34.0433, -118.2672, 0.85],
        
        // Pershing Square area (medium density)
        [34.0484, -118.2518, 0.6],
        [34.0483, -118.2520, 0.65],
        [34.0485, -118.2519, 0.7],
        
        // Grand Central Market area (high density)
        [34.0508, -118.2498, 0.85],
        [34.0507, -118.2497, 0.8],
        [34.0509, -118.2496, 0.9],
        
        // Union Station (medium-high density)
        [34.0561, -118.2365, 0.75],
        [34.0562, -118.2366, 0.8],
        [34.0560, -118.2367, 0.7],
        
        // Walt Disney Concert Hall (medium density)
        [34.0553, -118.2497, 0.6],
        [34.0552, -118.2496, 0.55],
        [34.0554, -118.2498, 0.65],
        
        // Little Tokyo (varying density)
        [34.0505, -118.2400, 0.7],
        [34.0504, -118.2401, 0.65],
        [34.0503, -118.2402, 0.75],
    ];

    // Add heat layer with custom gradient
    const heat = L.heatLayer(heatData, {
        radius: 35,
        blur: 25,
        maxZoom: 15,
        max: 1.0,
        gradient: {
            0.2: '#0571b0',  // Low density - cool blue
            0.4: '#92c5de',  // Low-medium density - light blue
            0.6: '#f7f7f7',  // Medium density - white
            0.8: '#f4a582',  // Medium-high density - light red
            1.0: '#ca0020'   // High density - deep red
        }
    }).addTo(map);

    // Add markers for key locations
    const locations = [
        {
            name: "LA Live",
            coords: [34.0430, -118.2673],
            risk: "High",
            density: "850 people"
        },
        {
            name: "Pershing Square",
            coords: [34.0484, -118.2518],
            risk: "Medium",
            density: "400 people"
        },
        {
            name: "Grand Central Market",
            coords: [34.0508, -118.2498],
            risk: "High",
            density: "750 people"
        }
    ];
// Update the crowd trend chart configuration
const crowdTrend = new Chart(
    document.getElementById('crowdTrend'),
    {
        type: 'line',
        data: {
            labels: ['12:00', '13:00', '14:00', '15:00', '16:00', '17:00'],
            datasets: [
                {
                    label: 'Location A',
                    data: [65, 70, 80, 85, 75, 82],
                    borderColor: '#e94560',
                    backgroundColor: 'rgba(233, 69, 96, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Location B',
                    data: [55, 60, 70, 75, 65, 72],
                    borderColor: '#ff6b6b',
                    backgroundColor: 'rgba(255, 107, 107, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Location C',
                    data: [45, 50, 60, 65, 55, 62],
                    borderColor: '#ff9f43',
                    backgroundColor: 'rgba(255, 159, 67, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        color: '#e94560',
                        font: {
                            family: 'Rajdhani',
                            size: 12
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Crowd Density Trends',
                    color: '#e94560',
                    font: {
                        family: 'Audiowide',
                        size: 16
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(233, 69, 96, 0.1)'
                    },
                    ticks: {
                        color: '#e94560',
                        font: {
                            family: 'Rajdhani'
                        }
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(233, 69, 96, 0.1)'
                    },
                    ticks: {
                        color: '#e94560',
                        font: {
                            family: 'Rajdhani'
                        }
                    }
                }
            }
        }
    }
);
    // Add custom markers with popups
    locations.forEach(loc => {
        const marker = L.marker(loc.coords)
            .bindPopup(`
                <div class="popup-content">
                    <h3>${loc.name}</h3>
                    <p>Risk Level: <span class="risk-${loc.risk.toLowerCase()}">${loc.risk}</span></p>
                    <p>Current Density: ${loc.density}</p>
                </div>
            `)
            .addTo(map);
    });
    // Add this function and interval here
    function updateMetrics() {
        const lightLevel = Math.floor(Math.random() * (500 - 400) + 400);
        const soundLevel = Math.floor(Math.random() * (75 - 55) + 55);
        const proximity = Math.floor(Math.random() * (90 - 70) + 70);
        const safetyScore = (Math.random() * (9.5 - 7.5) + 7.5).toFixed(1);

        document.querySelector('.metric-card:nth-child(1) .value').textContent = lightLevel;
        document.querySelector('.metric-card:nth-child(2) .value').textContent = soundLevel;
        document.querySelector('.metric-card:nth-child(3) .value').textContent = proximity;
        document.querySelector('.safety-score').textContent = safetyScore;
    }

    // Call updateMetrics every 5 seconds
    setInterval(updateMetrics, 5000);
    
    // Initial call to set values immediately
    updateMetrics();
    // Update heat data periodically to simulate real-time changes
    setInterval(() => {
        const updatedHeatData = heatData.map(point => {
            // Add small random variations to the intensity
            return [
                point[0],
                point[1],
                Math.min(1, Math.max(0.2, point[2] + (Math.random() - 0.5) * 0.1))
            ];
        });
        heat.setLatLngs(updatedHeatData);
    }, 5000);
});