/**
 * Dr Sam: a code-drawn, gender-neutral SVG avatar (decision D-07, step one).
 * Expression comes from the agent's own move, never from the person's tone label
 * (D-10). The mouth is driven by a viseme id while speaking.
 */
import { useEffect, useState } from "react";

export type Expression = "attentive" | "listening" | "thoughtful" | "warm" | "concerned" | "reassuring_neutral" | "serious" | "speaking";

type Props = { expression: Expression; viseme: number; speaking: boolean; reducedMotion?: boolean; size?: number };

const BROWS: Record<Expression, { l: string; r: string }> = {
  attentive: { l: "M62 82 Q78 74 94 80", r: "M106 80 Q122 74 138 82" },
  listening: { l: "M62 79 Q78 70 94 77", r: "M106 77 Q122 70 138 79" },
  thoughtful: { l: "M62 80 Q78 76 94 84", r: "M106 78 Q122 68 138 78" },
  warm: { l: "M62 82 Q78 74 94 80", r: "M106 80 Q122 74 138 82" },
  concerned: { l: "M62 78 Q80 84 94 88", r: "M106 88 Q120 84 138 78" },
  reassuring_neutral: { l: "M62 82 Q78 76 94 81", r: "M106 81 Q122 76 138 82" },
  serious: { l: "M62 84 Q78 80 94 84", r: "M106 84 Q122 80 138 84" },
  speaking: { l: "M62 82 Q78 74 94 80", r: "M106 80 Q122 74 138 82" },
};

const MOUTH_BY_VISEME: Record<number, string> = {
  0: "M80 142 Q100 150 120 142", // rest
  1: "M82 138 Q100 162 118 138 Q100 146 82 138", // open
  2: "M76 140 Q100 152 124 140 Q100 148 76 140", // wide
  3: "M90 136 Q100 158 110 136 Q100 144 90 136", // round
  4: "M82 142 Q100 144 118 142", // closed
};

const MOUTH_BY_EXPRESSION: Partial<Record<Expression, string>> = {
  warm: "M78 140 Q100 158 122 140",
  concerned: "M82 146 Q100 138 118 146",
  serious: "M84 144 L116 144",
  thoughtful: "M84 144 Q100 146 116 143",
  reassuring_neutral: "M80 142 Q100 152 120 142",
  listening: "M82 142 Q100 149 118 142",
};

export function Avatar({ expression, viseme, speaking, reducedMotion, size = 240 }: Props) {
  const [blink, setBlink] = useState(false);
  const [drift, setDrift] = useState({ x: 0, y: 0 });

  useEffect(() => {
    let alive = true;
    const loop = () => {
      if (!alive) return;
      const wait = 3000 + Math.random() * 3000;
      setTimeout(() => {
        if (!alive) return;
        setBlink(true);
        setTimeout(() => setBlink(false), 120);
        loop();
      }, wait);
    };
    loop();
    return () => {
      alive = false;
    };
  }, []);

  useEffect(() => {
    if (reducedMotion) return;
    const id = setInterval(() => setDrift({ x: (Math.random() - 0.5) * 3, y: (Math.random() - 0.5) * 2 }), 2200);
    return () => clearInterval(id);
  }, [reducedMotion]);

  const tilt = expression === "warm" ? -3 : expression === "concerned" ? 2 : 0;
  const nod = expression === "listening" && !reducedMotion ? "nod" : "";
  const mouth = speaking ? MOUTH_BY_VISEME[viseme] || MOUTH_BY_VISEME[0] : MOUTH_BY_EXPRESSION[expression] || MOUTH_BY_VISEME[0];
  const brows = BROWS[expression] || BROWS.attentive;
  const gazeUp = expression === "thoughtful" ? -3 : 0;
  const eyeH = blink ? 1 : expression === "serious" ? 8 : 9;

  return (
    <svg viewBox="0 0 200 220" width={size} height={size * 1.1} role="img" aria-label={`Dr Sam, ${expression.replace("_", " ")}`} className={`avatar ${nod}`}>
      <defs>
        <linearGradient id="skin" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0" stopColor="var(--skin-hi)" />
          <stop offset="1" stopColor="var(--skin)" />
        </linearGradient>
      </defs>
      <g transform={`translate(${drift.x} ${drift.y}) rotate(${tilt} 100 120)`} style={{ transition: "transform 450ms ease" }}>
        {/* shoulders and jacket */}
        <path d="M20 220 Q30 176 70 168 L100 176 L130 168 Q170 176 180 220 Z" fill="var(--jacket)" />
        <path d="M84 168 L100 182 L116 168 L100 176 Z" fill="var(--shirt)" />
        <rect x="96" y="176" width="8" height="30" fill="var(--lanyard)" />
        {/* neck */}
        <rect x="86" y="150" width="28" height="26" rx="8" fill="url(#skin)" />
        {/* hair back */}
        <path d="M48 96 Q44 40 100 36 Q156 40 152 96 L152 116 L48 116 Z" fill="var(--hair)" />
        {/* face */}
        <path d="M52 92 Q52 44 100 44 Q148 44 148 92 L148 118 Q148 162 100 166 Q52 162 52 118 Z" fill="url(#skin)" />
        {/* hair front, neutral short cut */}
        <path d="M52 92 Q58 52 100 50 Q142 52 148 92 Q140 66 100 64 Q60 66 52 92 Z" fill="var(--hair)" />
        {/* ears */}
        <ellipse cx="52" cy="106" rx="6" ry="10" fill="var(--skin)" />
        <ellipse cx="148" cy="106" rx="6" ry="10" fill="var(--skin)" />
        {/* glasses */}
        <g stroke="var(--frame)" strokeWidth="2.5" fill="none">
          <rect x="62" y="94" width="32" height="22" rx="8" />
          <rect x="106" y="94" width="32" height="22" rx="8" />
          <path d="M94 104 L106 104" />
          <path d="M62 102 L54 100" />
          <path d="M138 102 L146 100" />
        </g>
        {/* eyes */}
        <g style={{ transition: "all 120ms" }}>
          <ellipse cx="78" cy={104 + gazeUp} rx="5" ry={eyeH / 2} fill="var(--eye)" />
          <ellipse cx="122" cy={104 + gazeUp} rx="5" ry={eyeH / 2} fill="var(--eye)" />
          <circle cx="79.5" cy={103 + gazeUp} r="1.4" fill="#fff" opacity={blink ? 0 : 0.9} />
          <circle cx="123.5" cy={103 + gazeUp} r="1.4" fill="#fff" opacity={blink ? 0 : 0.9} />
        </g>
        {/* brows */}
        <g stroke="var(--hair)" strokeWidth="3.5" strokeLinecap="round" fill="none" style={{ transition: "d 400ms" }}>
          <path d={brows.l} />
          <path d={brows.r} />
        </g>
        {/* nose */}
        <path d="M100 108 Q96 124 100 128 Q104 124 100 108" stroke="var(--skin-line)" strokeWidth="2" fill="none" strokeLinecap="round" />
        {/* mouth */}
        <path d={mouth} stroke="var(--mouth)" strokeWidth="3" strokeLinecap="round" fill={speaking && viseme !== 0 && viseme !== 4 ? "var(--mouth-in)" : "none"} style={{ transition: speaking ? "d 60ms" : "d 350ms" }} />
      </g>
    </svg>
  );
}
