// ============================================================
// shared.js — Claude Code Intro Site
// ============================================================

// ---- Progress Bar ----
const progress = document.getElementById('progress');
if (progress) {
  window.addEventListener('scroll', () => {
    const h = document.documentElement;
    const pct = (h.scrollTop / (h.scrollHeight - h.clientHeight)) * 100;
    progress.style.width = pct + '%';
  }, { passive: true });
}

// ---- Scroll Reveal ----
const reveals = document.querySelectorAll('.reveal');
const revealObs = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) e.target.classList.add('in');
  });
}, { threshold: 0.1, rootMargin: '0px 0px -6% 0px' });
reveals.forEach(el => revealObs.observe(el));

// ---- Showcase staggered reveal ----
const showcaseInners = document.querySelectorAll('.showcase-inner');
const showcaseObs = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) e.target.classList.add('in');
  });
}, { threshold: 0.15, rootMargin: '0px 0px -8% 0px' });
showcaseInners.forEach(el => showcaseObs.observe(el));

// ---- Tab Switching ----
document.querySelectorAll('.tab-group').forEach(group => {
  const tabs = group.querySelectorAll('.tab');
  const contents = group.querySelectorAll('.tab-content');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const t = tab.dataset.tab;
      tabs.forEach(x => x.classList.remove('active'));
      contents.forEach(x => x.classList.remove('active'));
      tab.classList.add('active');
      group.querySelector(`[data-content="${t}"]`).classList.add('active');
    });
  });
});

// ---- Copy Code ----
document.querySelectorAll('.code-block').forEach(block => {
  const btn = block.querySelector('.copy-btn');
  if (!btn) return;
  btn.addEventListener('click', async () => {
    const code = block.querySelector('code').textContent;
    try {
      await navigator.clipboard.writeText(code);
      btn.textContent = 'Copied!';
      btn.style.color = 'var(--term-green)';
      setTimeout(() => { btn.textContent = 'Copy'; btn.style.color = ''; }, 1800);
    } catch {
      btn.textContent = 'Failed';
      setTimeout(() => { btn.textContent = 'Copy'; }, 1800);
    }
  });
});

// ---- Smooth anchor scroll ----
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    e.preventDefault();
    const target = document.querySelector(a.getAttribute('href'));
    if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});

// ---- Nav scroll active ----
function updateNavActive() {
  const sections = document.querySelectorAll('section[id]');
  const links = document.querySelectorAll('.nav-links a');
  let current = '';
  sections.forEach(s => {
    if (window.scrollY >= s.offsetTop - 200) current = s.getAttribute('id');
  });
  links.forEach(link => {
    link.classList.remove('active');
    if (link.getAttribute('href') === '#' + current) link.classList.add('active');
  });
}
window.addEventListener('scroll', updateNavActive, { passive: true });

// ============================================================
// DECODE EFFECT — global, reusable
// ============================================================
const DECODE_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*<>{}[]|/\\~`中文解码';

function decodeRun(el, opts) {
  const {
    delay = 0,
    charSpeed = 50,
    cycles = 10,
    color = 'var(--term-green)',
    glow = 'rgba(45, 212, 168, 0.25)',
    duration = 500,
  } = opts || {};

  const final = el.dataset.text;
  if (!final) return;
  el.textContent = '';
  el.classList.add('decode-active');

  const spans = [];
  for (let i = 0; i < final.length; i++) {
    const s = document.createElement('span');
    s.textContent = DECODE_CHARS[Math.floor(Math.random() * DECODE_CHARS.length)];
    s.style.opacity = '0';
    el.appendChild(s);
    spans.push(s);
  }

  // Phase in: each char appears
  spans.forEach((s, i) => {
    setTimeout(() => { s.style.opacity = '1'; }, delay + i * 28);
  });

  // Phase scramble → resolve
  spans.forEach((s, i) => {
    let cycle = 0;
    const id = setInterval(() => {
      s.textContent = DECODE_CHARS[Math.floor(Math.random() * DECODE_CHARS.length)];
      cycle++;
      if (cycle >= cycles) {
        clearInterval(id);
        s.textContent = final[i];
        s.style.color = color;
        s.style.textShadow = `0 0 8px ${glow}`;
        setTimeout(() => { s.style.color = ''; s.style.textShadow = ''; }, duration);
      }
    }, charSpeed);
  });
}

// Auto-init: hero elements fire immediately, others on scroll
(function() {
  const decodeEls = document.querySelectorAll('.decode');
  if (!decodeEls.length) return;

  decodeEls.forEach(el => {
    if (el.dataset.decodeHero !== undefined) {
      // Hero element: fire after short delay
      const heroDelay = parseInt(el.dataset.decodeDelay || '800', 10);
      setTimeout(() => decodeRun(el, { delay: 0, cycles: 12, charSpeed: 50 }), heroDelay);
    } else {
      // Scroll-triggered: use IntersectionObserver
      let fired = false;
      const obs = new IntersectionObserver(entries => {
        entries.forEach(e => {
          if (e.isIntersecting && !fired) {
            fired = true;
            obs.unobserve(el);
            decodeRun(el, { delay: 100, cycles: 8, charSpeed: 40 });
          }
        });
      }, { threshold: 0.3 });
      obs.observe(el);
    }
  });
})();

// ============================================================
// BUTTON RIPPLE
// ============================================================
document.querySelectorAll('.btn').forEach(btn => {
  btn.addEventListener('click', function(e) {
    const rect = this.getBoundingClientRect();
    const ripple = document.createElement('span');
    ripple.className = 'ripple';
    const size = Math.max(rect.width, rect.height);
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = (e.clientX - rect.left - size / 2) + 'px';
    ripple.style.top = (e.clientY - rect.top - size / 2) + 'px';
    this.appendChild(ripple);
    setTimeout(() => ripple.remove(), 600);
  });
});

// ============================================================
// COUNTER ANIMATION
// ============================================================
(function() {
  const allStats = document.querySelectorAll('.stat-num');
  if (!allStats.length) return;

  let fired = false;
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting && !fired) {
        fired = true;
        obs.disconnect();
        allStats.forEach(el => {
          // Static content (∞) — just reveal
          if (el.dataset.static) {
            el.textContent = el.dataset.static;
            return;
          }
          const target = parseInt(el.dataset.count, 10);
          const prefix = el.dataset.prefix || '';
          const suffix = el.dataset.suffix || '';
          if (isNaN(target) || target === 0) return;

          let current = 0;
          const step = Math.max(1, Math.ceil(target / 40));
          const interval = setInterval(() => {
            current += step;
            if (current >= target) {
              current = target;
              clearInterval(interval);
            }
            el.textContent = prefix + current + suffix;
          }, 30);
        });
      }
    });
  }, { threshold: 0.3 });

  allStats.forEach(el => obs.observe(el));
})();

// ============================================================
// GLOW CURSOR BALL
// ============================================================
(function() {
  // Skip on touch devices
  if ('ontouchstart' in window) return;

  const COLORS = {
    'index.html':    { core: '#FF5F57', glow: 'rgba(255,95,87,' },
    'install.html':  { core: '#FFBD2E', glow: 'rgba(255,189,46,' },
    'usage.html':    { core: '#2DD4A8', glow: 'rgba(45,212,168,' },
    'experience.html': { core: '#A78BFA', glow: 'rgba(167,139,250,' },
  };

  const page = location.pathname.split('/').pop() || 'index.html';
  const c = COLORS[page] || COLORS['index.html'];

  const ball = document.createElement('div');
  ball.className = 'cursor-ball';
  ball.style.background = `radial-gradient(circle, ${c.core}99 0%, ${c.glow}0.15) 50%, transparent 70%)`;
  ball.style.boxShadow = `0 0 20px ${c.glow}0.4), 0 0 40px ${c.glow}0.15)`;
  document.body.appendChild(ball);

  let mx = -100, my = -100;
  let bx = -100, by = -100;

  document.addEventListener('mousemove', e => {
    mx = e.clientX;
    my = e.clientY;
  });

  // Hover state on interactive elements
  const hoverEls = 'a, button, .btn, .tab, .code-block, .copy-btn, .card, .layer-card, .showcase-inner';
  document.addEventListener('mouseover', e => {
    if (e.target.closest(hoverEls)) ball.classList.add('hover');
  });
  document.addEventListener('mouseout', e => {
    if (e.target.closest(hoverEls)) ball.classList.remove('hover');
  });

  // Heading color influence — cursor tints h1/h2/h3 to cursor color
  const headings = document.querySelectorAll('h1, h2, h3');
  headings.forEach(h => {
    h.style.transition = 'color 0.3s ease';
    h.addEventListener('mouseenter', () => { h.style.color = c.core; });
    h.addEventListener('mouseleave', () => { h.style.color = ''; });
  });

  // Smooth follow with lerp
  function tick() {
    bx += (mx - bx) * 0.15;
    by += (my - by) * 0.15;
    ball.style.left = bx + 'px';
    ball.style.top = by + 'px';
    requestAnimationFrame(tick);
  }
  tick();
})();
