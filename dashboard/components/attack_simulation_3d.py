import streamlit.components.v1 as components

def render_3d_simulation(attack_event=None):
    """
    Renders an interactive Three.js component for the quantum attack simulation.
    attack_event (dict): Optional dict with keys: type, intensity, classification, status
    """
    
    # Extract properties
    a_type = attack_event.get("type", "") if attack_event else ""
    a_intent = attack_event.get("intensity", 0.0) if attack_event else 0.0
    a_class = attack_event.get("classification", "") if attack_event else ""
    a_status = attack_event.get("status", "NORMAL") if attack_event else "NORMAL"
    
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                overflow: hidden;
                background-color: #000000;
                font-family: 'Courier New', Courier, monospace;
                color: #00FF41;
            }}
            #canvas-container {{
                width: 100%;
                height: 500px;
                position: relative;
            }}
            #overlay {{
                position: absolute;
                top: 10px;
                left: 10px;
                z-index: 10;
                pointer-events: none;
                background: rgba(0,20,0,0.7);
                padding: 10px;
                border: 1px solid #00FF41;
                border-radius: 5px;
            }}
            .panel-title {{
                font-weight: bold;
                margin-bottom: 5px;
                font-size: 1.2em;
            }}
            .status-text {{
                font-size: 0.9em;
                color: #FFFF00;
            }}
            .threat-text {{
                color: #FF0000;
                font-weight: bold;
            }}
            .green-text {{
                color: #00FF41;
            }}
        </style>
    </head>
    <body>
        <div id="canvas-container">
            <div id="overlay">
                <div class="panel-title">QVERIS SOC TRACE</div>
                <div id="state-text" class="status-text">STATE: {a_status}</div>
                <div id="analysis-text" style="display:none; font-size:0.8em; margin-top:5px;"></div>
            </div>
        </div>

        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        
        <script>
            const a_type = "{a_type}";
            const a_intent = {a_intent};
            const a_class = "{a_class}";
            const a_status = "{a_status}"; // NORMAL or RUNNING

            const container = document.getElementById('canvas-container');
            const stateEl = document.getElementById('state-text');
            const analysisEl = document.getElementById('analysis-text');

            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x000000);
            
            const camera = new THREE.PerspectiveCamera(50, window.innerWidth / 500, 0.1, 1000);
            camera.position.set(0, 2, 12);
            
            const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
            renderer.setSize(window.innerWidth, 500);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            container.appendChild(renderer.domElement);

            window.addEventListener('resize', () => {{
                camera.aspect = window.innerWidth / 500;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, 500);
            }});

            // SHARED MATERIALS
            const greenMat = new THREE.MeshBasicMaterial({{ color: 0x00FF41, wireframe: true }});
            const solidGreen = new THREE.MeshBasicMaterial({{ color: 0x00FF41, transparent: true, opacity: 0.8 }});
            const redMat = new THREE.MeshBasicMaterial({{ color: 0xFF0000, transparent: true, opacity: 0.8 }});
            const yellowMat = new THREE.MeshBasicMaterial({{ color: 0xFFFF00, wireframe: true }});
            const cyanMat = new THREE.MeshBasicMaterial({{ color: 0x00FFFF, transparent: true, opacity: 0.8 }});

            // NODES
            const nodeGeo = new THREE.OctahedronGeometry(0.8, 1);
            
            const alice = new THREE.Mesh(nodeGeo, greenMat.clone());
            alice.position.set(-6, 0, 0);
            scene.add(alice);

            const bob = new THREE.Mesh(nodeGeo, greenMat.clone());
            bob.position.set(6, 0, 0);
            scene.add(bob);

            const attacker = new THREE.Mesh(new THREE.OctahedronGeometry(0.6, 0), redMat.clone());
            attacker.position.set(0, 4, 0);
            attacker.visible = false;
            scene.add(attacker);

            // CHANNEL
            let linkGeo = new THREE.BufferGeometry().setFromPoints([alice.position, bob.position]);
            let linkMat = new THREE.LineDashedMaterial({{ color: 0x00FF41, dashSize: 0.2, gapSize: 0.2 }});
            let channel = new THREE.Line(linkGeo, linkMat);
            channel.computeLineDistances();
            scene.add(channel);

            // PARTICLES / PULSES
            const pulseGeo = new THREE.SphereGeometry(0.3, 8, 8);
            const pulse = new THREE.Mesh(pulseGeo, cyanMat.clone());
            pulse.visible = false;
            scene.add(pulse);

            const forgePulse = new THREE.Mesh(pulseGeo, redMat.clone());
            forgePulse.visible = false;
            scene.add(forgePulse);

            // SCANNER / MEASUREMENT
            const scanGeo = new THREE.TorusGeometry(1.2, 0.05, 16, 100);
            const scanner = new THREE.Mesh(scanGeo, yellowMat.clone());
            scanner.rotation.x = Math.PI / 2;
            scanner.visible = false;
            scene.add(scanner);
            
            // BACKGROUND GRID
            const gridGeo = new THREE.BufferGeometry();
            const gridPos = new Float32Array(500 * 3);
            for(let i=0; i<1500; i++) {{
                gridPos[i] = (Math.random() - 0.5) * 30;
            }}
            gridGeo.setAttribute('position', new THREE.BufferAttribute(gridPos, 3));
            let gridMat = new THREE.PointsMaterial({{ color: 0x003311, size: 0.1 }});
            const grid = new THREE.Points(gridGeo, gridMat);
            scene.add(grid);

            // TEXT LABELS (Canvas based)
            function makeTextLabel(text, position) {{
                // Fallback to simple sprite or let's just stick to HTML overlay for labels
            }}

            let startTime = performance.now();
            let phase = 0;

            function updateOverlay(text, alertLevel=0) {{
                analysisEl.style.display = 'block';
                analysisEl.innerText = text;
                if (alertLevel === 2) analysisEl.className = "threat-text";
                else if (alertLevel === 1) analysisEl.className = "status-text";
                else analysisEl.className = "green-text";
            }}

            function animate() {{
                requestAnimationFrame(animate);
                let time = (performance.now() - startTime) / 1000;
                
                // Idle rotations
                alice.rotation.y += 0.01;
                bob.rotation.y -= 0.01;
                grid.rotation.y += 0.001;

                if (a_status === "RUNNING") {{
                    // Execute specific visual routines based on time
                    if (time < 1.0) {{
                        if(phase !== 1) {{
                            phase = 1;
                            stateEl.innerText = "STATE: ATTACK INITIALIZING";
                            updateOverlay("Preparing Quantum State...", 1);
                        }}
                    }}
                    else if (time < 4.0) {{
                        let tLocal = time - 1.0;
                        if(phase !== 2) {{
                            phase = 2;
                            stateEl.innerText = "STATE: ATTACK ACTIVE (" + a_type + ")";
                        }}
                        
                        // Default Pulse movement (Alice -> Bob)
                        pulse.visible = true;
                        let progress = (tLocal % 1.5) / 1.5; 
                        pulse.position.lerpVectors(alice.position, bob.position, progress);
                        
                        // Attack Variations
                        if (a_type === "FORGERY") {{
                            // Show a normal pulse sometimes, then a red pulse
                            if (tLocal > 1.5) {{
                                pulse.visible = false;
                                forgePulse.visible = true;
                                let forgeP = ((tLocal - 1.5) % 1.5) / 1.5;
                                forgePulse.position.lerpVectors(alice.position, bob.position, forgeP);
                                updateOverlay("Forged signature packet entering channel...", 2);
                            }} else {{
                                updateOverlay("Legitimate packet trace normal.", 0);
                            }}
                        }} 
                        else if (a_type === "IMPERSONATION") {{
                            attacker.visible = true;
                            // Attacker tries to connect
                            let attP = tLocal / 3.0; // 0 to 1
                            attacker.position.set(-6 + (6*attP), 4 - (4*attP), 0);
                            
                            forgePulse.visible = true;
                            let pulseP = (tLocal % 1.0);
                            forgePulse.position.lerpVectors(attacker.position, bob.position, pulseP);
                            updateOverlay("Identity mismatch! Untrusted node detected.", 2);
                        }}
                        else if (a_type === "REPLAY") {{
                            updateOverlay("Duplicate session context observed (Replay).", 2);
                            // Two identical pulses tracking closely
                            forgePulse.visible = true;
                            let forgeP = Math.max(0, progress - 0.2);
                            forgePulse.position.lerpVectors(alice.position, bob.position, forgeP);
                            forgePulse.material.color = new THREE.Color(0x00FFFF); // Copy cat
                        }}
                        else if (a_type === "UNAUTHORIZED_VERIFICATION") {{
                            updateOverlay("Unauthorized observer requesting access...", 2);
                            attacker.visible = true;
                            attacker.position.set(0, 0, 3);
                            // Ray from attacker to channel
                            channel.material.color.setHex(0xFFFF00);
                        }}
                        else if (a_type === "CHANNEL_MANIPULATION") {{
                            updateOverlay(`Channel manipulation intensity: ${{a_intent.toFixed(2)}}`, 2);
                            // Distort the channel line heavily
                            let wave = Math.sin(tLocal * 20 * a_intent) * 2;
                            channel.position.y = wave;
                            channel.material.color.setHex(0xFF0000);
                            pulse.position.y += (Math.random()-0.5) * a_intent * 3;
                        }}

                    }}
                    else if (time < 5.5) {{
                        if (phase !== 3) {{
                            phase = 3;
                            stateEl.innerText = "STATE: QUANTUM MEASUREMENT";
                            updateOverlay("Projective Measurement on Z/X basis...", 1);
                            pulse.visible = false;
                            forgePulse.visible = false;
                            attacker.visible = false;
                            
                            // Return channel to normal
                            channel.position.y = 0;
                            channel.material.color.setHex(0x00FF41);

                            // Apply scanner on Bob
                            scanner.visible = true;
                            scanner.position.copy(bob.position);
                        }}
                        scanner.scale.setScalar(1 + Math.sin(time*20)*0.2);
                        scanner.rotation.y += 0.1;
                    }}
                    else if (time < 7.0) {{
                        if (phase !== 4) {{
                            phase = 4;
                            stateEl.innerText = "STATE: ANALYSIS";
                            updateOverlay("Calculating Anomaly Distribution...", 1);
                            scanner.material.color.setHex(0x00FF41);
                            scanner.position.copy(alice.position); // Scan Alice too
                        }}
                        scanner.scale.setScalar(1 + Math.sin(time*30)*0.1);
                    }}
                    else {{
                        if (phase !== 5) {{
                            phase = 5;
                            scanner.visible = false;
                            let fState = "RESULT: " + a_class;
                            stateEl.innerText = fState;

                            if (a_class === "THREAT") {{
                                updateOverlay(a_type + " DETECTED. Action: REJECTED.", 2);
                                stateEl.className = "threat-text";
                                // Bob turns red
                                bob.material.color.setHex(0xFF0000);
                                channel.material.color.setHex(0xFF0000);
                            }} else if (a_class === "SUSPICIOUS") {{
                                updateOverlay(a_type + " SUSPICIOUS. Action: FLAG.", 1);
                                stateEl.className = "status-text";
                                bob.material.color.setHex(0xFFFF00);
                            }} else {{
                                updateOverlay("ALL CLEAR. Action: VERIFIED.", 0);
                                stateEl.className = "green-text";
                                bob.material.color.setHex(0x00FF41);
                            }}
                        }}
                    }}
                }}
                
                renderer.render(scene, camera);
            }}

            animate();
        </script>
    </body>
    </html>
    """
    
    components.html(html_template, height=500, scrolling=False)
