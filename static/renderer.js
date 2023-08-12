// renderer.js
let scene = new THREE.Scene();
scene.background = new THREE.Color(0xffffff); // Set the background color to white
let camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
let renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

fetch('/box')
    .then(response => response.json())
    .then(data => {
        // Create the box geometry from the data received from FastAPI
        let geometry = new THREE.BoxGeometry(data.width, data.height, data.depth);

        // Surface material: wood-like brown
        let material = new THREE.MeshBasicMaterial({color: 0x8B4513});
        let cube = new THREE.Mesh(geometry, material);

        // Edge material: black
        let edges = new THREE.EdgesGeometry(geometry);
        let line = new THREE.LineSegments(edges, new THREE.LineBasicMaterial({color: 0x000000}));

        // Add both cube and line to a group so they rotate together
        let group = new THREE.Group();
        group.add(cube);
        group.add(line);

        scene.add(group);

        camera.position.z = 5;

        // Render loop with added rotation
        function animate() {
            requestAnimationFrame(animate);
            group.rotation.x += 0.005;
            group.rotation.y += 0.005;
            renderer.render(scene, camera);
        }

        animate();
    });
