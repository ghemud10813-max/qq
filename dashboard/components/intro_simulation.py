import streamlit as st
import streamlit.components.v1 as components

def render_intro():
    """
    Renders a full-screen Three.js cinematic startup simulation logic.
    Only runs once per session.
    """
    if st.session_state.get('intro_played', False):
        return
        
    # We will mark it as played immediately so it doesn't re-render on python reruns
    st.session_state.intro_played = True
    
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            body, html {
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                overflow: hidden;
                background-color: #000000;
                font-family: 'Courier New', Courier, monospace;
            }
            #canvas-container {
                width: 100%;
                height: 100%;
                position: absolute;
                top: 0;
                left: 0;
                z-index: 10;
            }
            #overlay-text {
                position: absolute;
                top: 25%;
                left: 50%;
                transform: translate(-50%, -50%);
                text-align: center;
                z-index: 20;
                width: 100%;
                pointer-events: none;
            }
            .title {
                color: #00FF41;
                font-size: 3em;
                font-weight: bold;
                letter-spacing: 5px;
                text-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
                margin-bottom: 20px;
                opacity: 0;
                transform: translateY(20px);
                transition: opacity 0.4s ease, transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
            }
            .subtitle {
                color: #00FF41;
                font-size: 1.5em;
                letter-spacing: 2px;
                opacity: 0;
                transform: translateY(20px);
                transition: opacity 0.4s ease, transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
            }
            .caption {
                color: #FFFF00; /* Yellow warning/processing */
                font-size: 1.2em;
                margin-top: 10px;
                opacity: 0;
                transform: translateY(20px);
                transition: opacity 0.4s ease, transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
            }
            .anomaly {
                color: #FF0000;
                text-shadow: 0 0 10px rgba(255, 0, 0, 0.8);
            }
            #skip-btn {
                position: absolute;
                bottom: 30px;
                right: 30px;
                padding: 10px 20px;
                background-color: transparent;
                color: rgba(0, 255, 65, 0.6);
                border: 1px solid rgba(0, 255, 65, 0.6);
                font-family: 'Courier New', Courier, monospace;
                font-size: 1em;
                cursor: pointer;
                z-index: 30;
                transition: all 0.3s ease;
            }
            #skip-btn:hover {
                background-color: rgba(0, 255, 65, 0.1);
                color: #00FF41;
                border: 1px solid #00FF41;
            }
        </style>
    </head>
    <body>
        <div id="canvas-container"></div>
        <div id="overlay-text">
            <div id="text-title" class="title"></div>
            <div id="text-subtitle" class="subtitle"></div>
            <div id="text-caption" class="caption"></div>
        </div>
        <button id="skip-btn">SKIP INTRO >></button>

        <!-- Using Three.js -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        
        <script>
            // --- STREAMLIT IFRAME HACK ---
            // Force this iframe to be fullscreen fixed overlay on parent window
            try {
                const frame = window.frameElement;
                if (frame) {
                    frame.style.position = 'fixed';
                    frame.style.top = '0';
                    frame.style.left = '0';
                    frame.style.width = '100vw';
                    frame.style.height = '100vh';
                    frame.style.zIndex = '999999';
                    frame.style.border = 'none';
                    frame.style.backgroundColor = '#000000';
                }
            } catch (e) {
                console.error("Frame access error (CORS/Cross-origin):", e);
            }

            function endSimulation() {
                try {
                    const frame = window.frameElement;
                    if (frame) {
                        frame.style.display = 'none';
                    }
                } catch (e) {}
                // Stop rendering
                cancelAnimationFrame(animationId);
                // Dispose contexts
                renderer.dispose();
                document.body.innerHTML = "";
            }

            document.getElementById('skip-btn').addEventListener('click', endSimulation);

            // --- THREE JS SETUP ---
            const container = document.getElementById('canvas-container');
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x000000);
            
            const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.z = 15;
            
            const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            container.appendChild(renderer.domElement);

            window.addEventListener('resize', () => {
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
            });

            // --- SHARED MATERIALS & GEOMETRIES ---
            const greenMat = new THREE.MeshBasicMaterial({ color: 0x00FF41, wireframe: true, transparent: true, opacity: 0 });
            const solidGreenMat = new THREE.MeshBasicMaterial({ color: 0x00FF41, transparent: true, opacity: 0 });
            const redMat = new THREE.MeshBasicMaterial({ color: 0xFF0000, transparent: true, opacity: 0 });
            const yellowMat = new THREE.MeshBasicMaterial({ color: 0xFFFF00, wireframe: true, transparent: true, opacity: 0 });
            
            // Group for central animations
            const centerGroup = new THREE.Group();
            centerGroup.position.y = -1.5;
            scene.add(centerGroup);

            // GRID PARTICLES
            let gridParticles;
            const particleCount = 1000;
            const particleGeo = new THREE.BufferGeometry();
            const particlePos = new Float32Array(particleCount * 3);
            for(let i=0; i<particleCount * 3; i++) {
                particlePos[i] = (Math.random() - 0.5) * 40;
            }
            particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePos, 3));
            let particleMat = new THREE.PointsMaterial({ color: 0x00FF41, size: 0.1, transparent: true, opacity: 0 });
            gridParticles = new THREE.Points(particleGeo, particleMat);
            scene.add(gridParticles);

            // BLOCH SPHERE (Phase 2)
            const blochGroup = new THREE.Group();
            const sphereGeo = new THREE.SphereGeometry(3, 16, 16);
            const blochSphere = new THREE.Mesh(sphereGeo, greenMat.clone());
            blochGroup.add(blochSphere);
            // Axis lines
            const lineMat = new THREE.LineBasicMaterial({ color: 0x00AA33, transparent: true, opacity: 0});
            // Z
            const zGeo = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(0,-4,0), new THREE.Vector3(0,4,0)]);
            blochGroup.add(new THREE.Line(zGeo, lineMat));
            // X
            const xGeo = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(-4,0,0), new THREE.Vector3(4,0,0)]);
            blochGroup.add(new THREE.Line(xGeo, lineMat));
            // Y
            const yGeo = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(0,0,-4), new THREE.Vector3(0,0,4)]);
            blochGroup.add(new THREE.Line(yGeo, lineMat));
            
            // State vector
            const arrowDir = new THREE.Vector3(1, 1, 1).normalize();
            const arrowOrigin = new THREE.Vector3(0, 0, 0);
            const stateVector = new THREE.ArrowHelper(arrowDir, arrowOrigin, 3, 0xFFFF00);
            blochGroup.add(stateVector);
            blochGroup.visible = false;
            centerGroup.add(blochGroup);

            // ENTANGLEMENT NODES (Phase 3)
            const entangleGroup = new THREE.Group();
            const nodeGeo = new THREE.SphereGeometry(1, 16, 16);
            const nodeA = new THREE.Mesh(nodeGeo, greenMat.clone());
            const nodeB = new THREE.Mesh(nodeGeo, greenMat.clone());
            nodeA.position.set(-5, 0, 0);
            nodeB.position.set(5, 0, 0);
            entangleGroup.add(nodeA);
            entangleGroup.add(nodeB);
            
            const linkGeo = new THREE.BufferGeometry().setFromPoints([nodeA.position, nodeB.position]);
            const linkMat = new THREE.LineDashedMaterial({ color: 0x00FF41, dashSize: 0.5, gapSize: 0.5, transparent: true, opacity: 0});
            const linkLine = new THREE.Line(linkGeo, linkMat);
            linkLine.computeLineDistances();
            entangleGroup.add(linkLine);
            entangleGroup.visible = false;
            centerGroup.add(entangleGroup);
            
            // PULSE / TELEPORT / VERIFY / THREAT
            const objGeo = new THREE.OctahedronGeometry(0.5);
            const flyingState = new THREE.Mesh(objGeo, solidGreenMat.clone());
            flyingState.position.set(-5, 1.5, 0);
            flyingState.visible = false;
            centerGroup.add(flyingState);

            const threatNode = new THREE.Mesh(objGeo, redMat.clone());
            threatNode.position.set(0, -3, 0);
            threatNode.visible = false;
            centerGroup.add(threatNode);
            
            // DOM ELEMENTS
            const titleEl = document.getElementById('text-title');
            const subEl = document.getElementById('text-subtitle');
            const capEl = document.getElementById('text-caption');

            function setText(t, s, c, colorClass="") {
                titleEl.style.opacity = 0;
                subEl.style.opacity = 0;
                capEl.style.opacity = 0;
                
                titleEl.style.transform = 'translateY(-20px)';
                subEl.style.transform = 'translateY(-20px)';
                capEl.style.transform = 'translateY(-20px)';
                
                setTimeout(() => {
                    titleEl.innerText = t;
                    subEl.innerText = s;
                    capEl.innerText = c;
                    
                    if (colorClass == "red") {
                        titleEl.className = "title anomaly"; 
                        subEl.className = "subtitle anomaly";
                        capEl.className = "caption anomaly";
                        titleEl.style.color = "#FF0000";
                        subEl.style.color = "#FF0000";
                        capEl.style.color = "#FF0000";
                    } else if (colorClass == "yellow") {
                        titleEl.className = "title"; 
                        subEl.className = "subtitle";
                        capEl.className = "caption";
                        titleEl.style.color = "#00FF41";
                        subEl.style.color = "#00FF41";
                        capEl.style.color = "#FFFF00";
                    } else {
                        titleEl.className = "title"; 
                        subEl.className = "subtitle";
                        capEl.className = "caption";
                        titleEl.style.color = "#00FF41";
                        subEl.style.color = "#00FF41";
                        capEl.style.color = "#00FF41"; // Use default green
                    }
                    
                    // Reset transform before fading in
                    titleEl.style.transform = 'translateY(20px)';
                    subEl.style.transform = 'translateY(20px)';
                    capEl.style.transform = 'translateY(20px)';
                    
                    // Force DOM reflow so shift is instant
                    void titleEl.offsetWidth; 
                    
                    titleEl.style.opacity = t ? 1 : 0;
                    subEl.style.opacity = s ? 1 : 0;
                    capEl.style.opacity = c ? 1 : 0;
                    
                    titleEl.style.transform = 'translateY(0px)';
                    subEl.style.transform = 'translateY(0px)';
                    capEl.style.transform = 'translateY(0px)';
                }, 400); // Wait for fade out
            }

            // --- ANIMATION LOOP ---
            let startTime = performance.now();
            let animationId;
            let currentPhase = -1;

            function animate() {
                animationId = requestAnimationFrame(animate);
                let time = (performance.now() - startTime) / 1000; // in seconds
                
                // Keep particles moving slowly
                gridParticles.rotation.y = time * 0.05;
                gridParticles.rotation.z = time * 0.02;

                // --- PHASE 1: Boot (0-2s) ---
                if (time < 2) {
                    if (currentPhase !== 0) {
                        currentPhase = 0;
                        setText("QVERIS", "QUANTUM SECURITY SYSTEM INITIALIZING...", "");
                    }
                    particleMat.opacity = Math.min(1, time / 1.5);
                }
                // --- PHASE 2: Quantum State (2-4s) ---
                else if (time < 4) {
                    if (currentPhase !== 1) {
                        currentPhase = 1;
                        setText("PREPARING QUANTUM STATE", "PAULI EIGENSTATE", "", "yellow");
                        blochGroup.visible = true;
                        blochSphere.material.opacity = 0;
                        lineMat.opacity = 0;
                    }
                    let progress = Math.min(1, (time - 2) * 2);
                    blochSphere.material.opacity = progress * 0.3;
                    lineMat.opacity = progress * 0.5;
                    
                    blochGroup.rotation.y += 0.02;
                    blochGroup.rotation.x += 0.01;
                    
                    // Rotate state vector around Z
                    const angle = time * Math.PI;
                    stateVector.setDirection(new THREE.Vector3(Math.cos(angle), Math.sin(angle), 1).normalize());
                }
                // --- PHASE 3: Entanglement (4-6s) ---
                else if (time < 6) {
                    if (currentPhase !== 2) {
                        currentPhase = 2;
                        setText("ESTABLISHING ENTANGLEMENT", "BELL STATE", "", "yellow");
                        blochGroup.visible = false;
                        entangleGroup.visible = true;
                        nodeA.material.opacity = 0;
                        nodeB.material.opacity = 0;
                        linkMat.opacity = 0;
                    }
                    let progress = Math.min(1, (time - 4) * 2);
                    nodeA.material.opacity = progress * 0.5;
                    nodeB.material.opacity = progress * 0.5;
                    linkMat.opacity = progress * 0.8;
                    
                    nodeA.rotation.y -= 0.05;
                    nodeB.rotation.y += 0.05;
                    
                    entangleGroup.rotation.z = Math.sin(time) * 0.2;
                }
                // --- PHASE 4: Teleportation (6-8s) ---
                else if (time < 8) {
                    if (currentPhase !== 3) {
                        currentPhase = 3;
                        setText("QUANTUM TELEPORTATION", "STATE TRANSFER + PAULI CORRECTION", "X/Z GATES APPLIED", "yellow");
                        flyingState.visible = true;
                        flyingState.material.opacity = 1;
                    }
                    
                    // Fly from A to B
                    let tProgress = (time - 6) / 2; // 0 to 1
                    flyingState.position.x = -5 + (tProgress * 10);
                    flyingState.position.y = Math.sin(tProgress * Math.PI) * 2.5; 
                    flyingState.rotation.x += 0.1;
                    flyingState.rotation.y += 0.2;
                }
                // --- PHASE 5: Verification (8-9.5s) ---
                else if (time < 9.5) {
                    if (currentPhase !== 4) {
                        currentPhase = 4;
                        setText("DIGITAL SIGNATURE VERIFICATION", "PROJECTIVE MEASUREMENT", "SUCCESS MATCH", "");
                        flyingState.visible = false;
                        entangleGroup.visible = false;
                        
                        // Bring bloch group back for measurement visual
                        blochGroup.visible = true;
                        blochSphere.material.opacity = 0.5;
                    }
                    blochGroup.scale.setScalar(1 + Math.sin(time * 20) * 0.1); // Pulse
                    blochGroup.rotation.y += 0.05;
                }
                // --- PHASE 6: Threat Detection (9.5-10.5s) ---
                else if (time < 10.5) {
                    if (currentPhase !== 5) {
                        currentPhase = 5;
                        setText("ANOMALY DETECTED", "THREAT ANALYSIS", "ISOLATING UNTRUSTED NODE", "red");
                        
                        threatNode.visible = true;
                        threatNode.material.opacity = 1;
                        blochGroup.visible = false;
                    }
                    threatNode.rotation.x += 0.2;
                    threatNode.rotation.y += 0.3;
                    threatNode.position.y = Math.sin(time * 15) * 0.5;
                    particleMat.color.setHex(0xFF0000); // Pulse grid red
                }
                // --- PHASE 7: Secure (10.5-11.5s) ---
                else if (time < 11.5) {
                    if (currentPhase !== 6) {
                        currentPhase = 6;
                        setText("SYSTEM SECURED", "", "");
                        
                        threatNode.visible = false;
                        particleMat.color.setHex(0x00FF41); // Grid back to green
                        
                        // Show massive green glow sphere
                        blochGroup.visible = true;
                        blochGroup.scale.setScalar(2);
                        blochSphere.material.opacity = 0.8;
                    }
                    blochGroup.rotation.y -= 0.1;
                }
                // --- PHASE 8: Brand Reveal (11.5-12.5s) ---
                else if (time < 12) {
                    if (currentPhase !== 7) {
                        currentPhase = 7;
                        setText("QVERIS", "QUANTUM VERIFICATION & RISK EVALUATION SYSTEM", "SYSTEM READY");
                        blochGroup.visible = false;
                    }
                    // Particles converge
                    let converge = (time - 11.5) * 5; // 0 to ~2.5
                    particleMat.size = 0.1 + converge * 0.2;
                    gridParticles.scale.setScalar(Math.max(0.01, 1 - converge * 0.5));
                } 
                // --- FINISH ---
                else {
                    endSimulation();
                }

                renderer.render(scene, camera);
            }

            // Start animation
            animate();
        </script>
    </body>
    </html>
    """
    
    components.html(html_code, height=0, width=0)
