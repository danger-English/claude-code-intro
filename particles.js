// ============================================================
// particles.js — Universal Starfield Background
// Four pages, each with its own accent color.
// ============================================================

(function () {
  if (typeof THREE === 'undefined') return;
  if ('ontouchstart' in window || window.innerWidth < 768) return;

  // ---- Page-specific accent colors ----
  const PAGE_COLORS = {
    'index.html':    { core: 0xf5a623, glow: 0x2dd4a8 },  // amber + green
    'install.html':  { core: 0xffbd2e, glow: 0xf5a623 },  // yellow + amber
    'usage.html':    { core: 0x2dd4a8, glow: 0xf5a623 },  // green + amber
    'skills.html':   { core: 0xf5a623, glow: 0x60a5fa },  // amber + blue
    'experience.html': { core: 0xf5a623, glow: 0xa78bfa }, // amber + purple
  };

  const page = location.pathname.split('/').pop() || 'index.html';
  const colors = PAGE_COLORS[page] || PAGE_COLORS['index.html'];

  // ---- Canvas ----
  const canvas = document.createElement('canvas');
  canvas.id = 'particle-canvas';
  canvas.style.cssText =
    'position:fixed;inset:0;width:100%;height:100%;z-index:0;pointer-events:none;';
  document.body.prepend(canvas);

  // ---- Renderer ----
  const renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: true,
    alpha: true,
    powerPreference: 'high-performance',
  });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setClearColor(0x000000, 0);

  // ---- Scene + Camera ----
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(
    60,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  );
  camera.position.z = 50;

  // ---- Mouse ----
  const mouse = { x: 0, y: 0, tx: 0, ty: 0 };
  document.addEventListener('mousemove', (e) => {
    mouse.tx = (e.clientX / window.innerWidth) * 2 - 1;
    mouse.ty = -(e.clientY / window.innerHeight) * 2 + 1;
  });

  // ---- Particles ----
  const COUNT = 2200;
  const SPREAD = 80;

  const posArr = new Float32Array(COUNT * 3);
  const velArr = new Float32Array(COUNT * 3);
  const sizeArr = new Float32Array(COUNT);
  const opaArr = new Float32Array(COUNT);
  const phaseArr = new Float32Array(COUNT);

  for (let i = 0; i < COUNT; i++) {
    const i3 = i * 3;
    posArr[i3]     = (Math.random() - 0.5) * SPREAD;
    posArr[i3 + 1] = (Math.random() - 0.5) * SPREAD;
    posArr[i3 + 2] = (Math.random() - 0.5) * SPREAD;
    velArr[i3]     = (Math.random() - 0.5) * 0.004;
    velArr[i3 + 1] = (Math.random() - 0.5) * 0.004;
    velArr[i3 + 2] = (Math.random() - 0.5) * 0.004;
    sizeArr[i]  = Math.random() * 2.4 + 0.6;
    opaArr[i]   = Math.random() * 0.5 + 0.35;
    phaseArr[i] = Math.random() * Math.PI * 2;
  }

  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(posArr, 3));
  geo.setAttribute('aSize',    new THREE.BufferAttribute(sizeArr, 1));
  geo.setAttribute('aOpacity', new THREE.BufferAttribute(opaArr, 1));
  geo.setAttribute('aPhase',   new THREE.BufferAttribute(phaseArr, 1));

  const mat = new THREE.ShaderMaterial({
    transparent: true,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
    uniforms: {
      uTime:       { value: 0 },
      uPixelRatio: { value: renderer.getPixelRatio() },
      uColor:      { value: new THREE.Color(colors.core) },
      uColor2:     { value: new THREE.Color(colors.glow) },
    },
    vertexShader: `
      attribute float aSize;
      attribute float aOpacity;
      attribute float aPhase;
      uniform float uTime;
      uniform float uPixelRatio;
      varying float vOpacity;
      varying float vPhase;
      void main() {
        vec3 p = position;
        p.y += sin(uTime * 0.25 + aPhase) * 0.6;
        p.x += cos(uTime * 0.18 + aPhase * 1.3) * 0.4;
        vec4 mv = modelViewMatrix * vec4(p, 1.0);
        gl_Position = projectionMatrix * mv;
        gl_PointSize = aSize * uPixelRatio * (80.0 / -mv.z);
        vOpacity = aOpacity;
        vPhase = aPhase;
      }
    `,
    fragmentShader: `
      uniform vec3 uColor;
      uniform vec3 uColor2;
      uniform float uTime;
      varying float vOpacity;
      varying float vPhase;
      void main() {
        float d = length(gl_PointCoord - vec2(0.5));
        if (d > 0.5) discard;
        float alpha = smoothstep(0.5, 0.0, d) * vOpacity;
        vec3 col = mix(uColor, uColor2, sin(uTime * 0.4 + vPhase) * 0.5 + 0.5);
        gl_FragColor = vec4(col, alpha);
      }
    `,
  });

  scene.add(new THREE.Points(geo, mat));

  // ---- Line connections ----
  const LINE_MAX = 300;
  const linePos = new Float32Array(LINE_MAX * 6);
  const lineGeo = new THREE.BufferGeometry();
  lineGeo.setAttribute('position', new THREE.BufferAttribute(linePos, 3));
  lineGeo.setDrawRange(0, 0);

  const lineMat = new THREE.LineBasicMaterial({
    color: colors.core,
    transparent: true,
    opacity: 0.1,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
  });
  scene.add(new THREE.LineSegments(lineGeo, lineMat));

  // ---- Animate ----
  const clock = new THREE.Clock();
  let raf;

  function tick() {
    raf = requestAnimationFrame(tick);
    const t = clock.getElapsedTime();

    mouse.x += (mouse.tx - mouse.x) * 0.05;
    mouse.y += (mouse.ty - mouse.y) * 0.05;

    const p = geo.attributes.position.array;
    const mx = mouse.x * 30;
    const my = mouse.y * 20;
    const half = SPREAD / 2;

    for (let i = 0; i < COUNT; i++) {
      const i3 = i * 3;
      p[i3]     += velArr[i3];
      p[i3 + 1] += velArr[i3 + 1];
      p[i3 + 2] += velArr[i3 + 2];

      // Mouse repulsion
      const dx = p[i3] - mx;
      const dy = p[i3 + 1] - my;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < 10 && dist > 0.01) {
        const f = (10 - dist) / 10;
        const nx = dx / dist;
        const ny = dy / dist;
        p[i3]     += nx * f * 0.25;
        p[i3 + 1] += ny * f * 0.25;
        p[i3]     -= nx * f * 0.04;
        p[i3 + 1] -= ny * f * 0.04;
      }

      // Wrap
      if (p[i3] > half) p[i3] = -half;
      if (p[i3] < -half) p[i3] = half;
      if (p[i3+1] > half) p[i3+1] = -half;
      if (p[i3+1] < -half) p[i3+1] = half;
      if (p[i3+2] > half) p[i3+2] = -half;
      if (p[i3+2] < -half) p[i3+2] = half;
    }

    geo.attributes.position.needsUpdate = true;
    mat.uniforms.uTime.value = t;

    // Lines
    let li = 0;
    const thresh = 5.5;
    const lp = lineGeo.attributes.position.array;
    const step = Math.max(1, Math.floor(COUNT / 500));
    for (let i = 0; i < COUNT && li < LINE_MAX; i += step) {
      const i3 = i * 3;
      for (let j = i + step; j < COUNT && li < LINE_MAX; j += step) {
        const j3 = j * 3;
        const dx = p[i3] - p[j3];
        const dy = p[i3+1] - p[j3+1];
        const dz = p[i3+2] - p[j3+2];
        if (dx*dx + dy*dy + dz*dz < thresh*thresh) {
          const o = li * 6;
          lp[o]   = p[i3];   lp[o+1] = p[i3+1]; lp[o+2] = p[i3+2];
          lp[o+3] = p[j3];   lp[o+4] = p[j3+1]; lp[o+5] = p[j3+2];
          li++;
        }
      }
    }
    lineGeo.setDrawRange(0, li * 2);
    lineGeo.attributes.position.needsUpdate = true;

    // Camera follow
    camera.position.x = mouse.x * 1.5;
    camera.position.y = mouse.y * 1;
    camera.lookAt(scene.position);

    renderer.render(scene, camera);
  }

  tick();

  // ---- Resize ----
  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    mat.uniforms.uPixelRatio.value = renderer.getPixelRatio();
  });

  // ---- Scroll fade ----
  window.addEventListener('scroll', () => {
    const ratio = 1 - window.scrollY / (window.innerHeight * 3);
    canvas.style.opacity = Math.max(0.15, Math.min(1, ratio));
  }, { passive: true });

  // ---- Pause when hidden ----
  document.addEventListener('visibilitychange', () => {
    document.hidden ? cancelAnimationFrame(raf) : tick();
  });
})();
