/* Hosts an original QVeris WebGL scene (dashboard/web/*) inside the app.
   Like dashboard/components/_web.py, the page template, the shared core.js and
   the scene entry are assembled into one ES module in a same-origin srcdoc
   iframe. three@0.165 is self-hosted under /vendor/three. Fresh data goes
   through window.__qvBus[channel], the bus the scenes already poll. */
import { useEffect, useMemo, useRef, useState } from 'react';

declare global { interface Window { __qvBus?: Record<string, { v: string; d: unknown }> } }

export type SceneName = 'story' | 'attack_lab' | 'noise' | 'verify';
const SOURCES: Record<SceneName, () => Promise<[string, string]>> = {
  story: () => Promise.all([import('./story.html?raw'), import('./story.js?raw')]).then(([a, b]) => [a.default, b.default]),
  attack_lab: () => Promise.all([import('./attack_lab.html?raw'), import('./attack_lab.js?raw')]).then(([a, b]) => [a.default, b.default]),
  noise: () => Promise.all([import('./panel.html?raw'), import('./noise_lab.js?raw')]).then(([a, b]) => [a.default, b.default]),
  verify: () => Promise.all([import('./panel.html?raw'), import('./verify_lab.js?raw')]).then(([a, b]) => [a.default, b.default]),
};
const loadCore = () => import('./core.js?raw').then((m) => m.default);

const MODULE_IMPORTS = `
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { FontLoader } from 'three/addons/loaders/FontLoader.js';
import { TextGeometry } from 'three/addons/geometries/TextGeometry.js';
`;

const jsonForScript = (d: unknown) => JSON.stringify(d).replace(/</g, '\\u003c');

async function buildDoc(scene: SceneName, data: Record<string, unknown>): Promise<string> {
  const [[template, entry], core] = await Promise.all([SOURCES[scene](), loadCore()]);
  const vendor = `${location.origin}/vendor/three`;
  const importMap = `<script type="importmap">${JSON.stringify({ imports: { three: `${vendor}/build/three.module.js`, 'three/addons/': `${vendor}/examples/jsm/` } })}</script>`;
  const script = `<script>window.QV_DATA = ${jsonForScript({ ...data, three_version: '0.165.0', vendor })};</script>\n` +
    `<script type="module">${MODULE_IMPORTS}\n${core}\n${entry}\n</script>`;
  return template.replace('<!--QV_HEAD-->', importMap).replace('<!--QV_SCRIPT-->', script);
}

let busSeq = 0;
export function publish(channel: string, payload: unknown) {
  window.__qvBus = window.__qvBus || {};
  window.__qvBus[channel] = { v: `v${++busSeq}`, d: payload };
}

interface Props {
  scene: SceneName; channel?: string; title?: string; data?: Record<string, unknown>; payload?: unknown;
  className?: string; style?: React.CSSProperties; label: string; onReady?: () => void;
}

export function LegacyScene({ scene, channel, title, data, payload, className, style, label, onReady }: Props) {
  const [doc, setDoc] = useState<string | null>(null);
  const [failed, setFailed] = useState(false);
  const ch = channel || scene;
  // The document is built once per mount: data that changes goes through the bus.
  const init = useMemo(() => ({ channel: ch, title, ...(data || {}) }), [ch]); // eslint-disable-line react-hooks/exhaustive-deps
  const ref = useRef<HTMLIFrameElement>(null);

  useEffect(() => {
    let alive = true;
    buildDoc(scene, init).then((d) => alive && setDoc(d)).catch(() => alive && setFailed(true));
    return () => { alive = false; };
  }, [scene, init]);

  useEffect(() => { if (payload !== undefined) publish(ch, payload); }, [ch, payload]);
  useEffect(() => () => { if (window.__qvBus) delete window.__qvBus[ch]; }, [ch]);

  if (failed || !webglAvailable()) {
    return <div className={`legacy-fallback ${className || ''}`} style={style} role="img" aria-label={label}>
      <div className="empty"><div className="orb" /><h4>3D scene unavailable</h4><p>This browser has no WebGL. All numbers remain available in the panels.</p></div>
    </div>;
  }
  return (
    <iframe
      ref={ref}
      className={`legacy-scene ${className || ''}`}
      style={style}
      title={label}
      aria-label={label}
      srcDoc={doc || '<!doctype html><html><body style="margin:0;background:#EAEDF7"></body></html>'}
      onLoad={() => doc && onReady?.()}
      allow="fullscreen"
    />
  );
}

let _webgl: boolean | null = null;
export function webglAvailable(): boolean {
  if (_webgl != null) return _webgl;
  try {
    const c = document.createElement('canvas');
    _webgl = !!(c.getContext('webgl2') || c.getContext('webgl'));
  } catch { _webgl = false; }
  return _webgl;
}
