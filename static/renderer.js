let scene = new THREE.Scene();
scene.background = new THREE.Color(0xffffff); // Set the background color to white
let camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
let renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

fetch('/collection')
    .then(response => response.json())
    .then(boxes => {
        boxes.forEach(data => {
            let width = data.end.x - data.start.x;
            let height = data.end.y - data.start.y;
            let depth = data.end.z - data.start.z;

            let geometry = new THREE.BoxGeometry(width, height, depth);

            // Surface material: wood-like brown
            let material = new THREE.MeshBasicMaterial({color: 0x8B4513});
            let cube = new THREE.Mesh(geometry, material);

            // Edge material: black
            let edges = new THREE.EdgesGeometry(geometry);
            let line = new THREE.LineSegments(edges, new THREE.LineBasicMaterial({color: 0x000000}));

            // Adjusting cube's position based on the start coordinates
            let posX = data.start.x + width/2;
            let posY = data.start.y + height/2;
            let posZ = data.start.z + depth/2;
            cube.position.set(posX, posY, posZ);

            // Set the position of the lines to match the cube's position
            line.position.set(posX, posY, posZ);

            // Add both cube and line to a group so they rotate together
            let group = new THREE.Group();
            group.add(cube);
            group.add(line);

            scene.add(group);
        });

        // Set the camera position dynamically based on the size of the box.
        // This is an approximation to make sure the camera is far enough from the objects to view them properly.
        let maxDimension = Math.max(boxes[0].end.x - boxes[0].start.x, boxes[0].end.y - boxes[0].start.y, boxes[0].end.z - boxes[0].start.z);
        camera.position.z = maxDimension * 3;

        // Render loop with added rotation
        function animate() {
            requestAnimationFrame(animate);
            scene.rotation.x += 0.005;
            scene.rotation.y += 0.005;
            renderer.render(scene, camera);
        }

        animate();
    });
