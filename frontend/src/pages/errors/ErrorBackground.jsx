export default function ErrorBackground() {
  return (
    <div className="error-bg-layer" aria-hidden="true">
      <div className="error-bg" />
      <div className="error-blob" />
      <svg className="error-contours" viewBox="0 0 400 280" fill="none" preserveAspectRatio="xMaxYMin slice">
        <path
          d="M120 40 C200 20, 280 60, 360 30"
          stroke="#52635a"
          strokeWidth="1.2"
          opacity="0.12"
        />
        <path
          d="M80 90 C180 70, 260 110, 380 80"
          stroke="#52635a"
          strokeWidth="1.2"
          opacity="0.1"
        />
        <path
          d="M140 140 C220 120, 300 160, 360 130"
          stroke="#52635a"
          strokeWidth="1.2"
          opacity="0.08"
        />
      </svg>
      <svg className="error-lines" viewBox="0 0 1200 800" fill="none" preserveAspectRatio="none">
        <path d="M-40 520 C180 420, 320 560, 520 480" />
        <path d="M680 120 C820 200, 960 80, 1180 160" />
        <path d="M200 680 C420 620, 560 740, 780 660" />
      </svg>
    </div>
  );
}
