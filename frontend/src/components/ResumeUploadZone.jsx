import { useRef } from "react";
import { IconUpload } from "./icons.jsx";

function formatFileSize(bytes) {
  if (!bytes) return "";
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export default function ResumeUploadZone({
  file,
  onFileChange,
  uploading = false,
  progress = null,
  idleLabel = "Drop your resume here, or choose a file",
}) {
  const inputRef = useRef(null);

  const handleReplace = () => {
    inputRef.current?.click();
  };

  if (!file) {
    return (
      <label className="resume-upload-zone resume-upload-zone--empty">
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.docx,.txt"
          onChange={(e) => onFileChange(e.target.files?.[0] || null)}
        />
        <span className="resume-upload-zone__icon" aria-hidden="true">
          <IconUpload size={28} />
        </span>
        <span className="resume-upload-zone__label">{idleLabel}</span>
        <span className="resume-upload-zone__hint">PDF, DOCX, or TXT · max 5 MB</span>
      </label>
    );
  }

  return (
    <div className={`resume-upload-zone resume-upload-zone--filled${uploading ? " resume-upload-zone--busy" : ""}`}>
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.docx,.txt"
        className="visually-hidden"
        onChange={(e) => onFileChange(e.target.files?.[0] || null)}
      />
      <div className="resume-upload-zone__file-row">
        <span className="resume-upload-zone__file-icon" aria-hidden="true">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
            <path d="M14 2v6h6M8 13h8M8 17h5" />
          </svg>
        </span>
        <div className="resume-upload-zone__meta">
          <strong>{file.name}</strong>
          <span>{formatFileSize(file.size)}</span>
        </div>
        <button type="button" className="resume-upload-zone__replace" onClick={handleReplace} disabled={uploading}>
          Replace file
        </button>
      </div>
      {uploading && (
        <>
          <p className="resume-upload-zone__status">Reading your resume…</p>
          <div className="resume-upload-zone__progress" role="progressbar" aria-valuenow={progress ?? 70} aria-valuemin="0" aria-valuemax="100">
            <span style={{ width: `${progress ?? 70}%` }} />
          </div>
        </>
      )}
    </div>
  );
}
