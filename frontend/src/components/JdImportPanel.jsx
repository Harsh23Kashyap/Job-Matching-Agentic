import Button from "./Button.jsx";

const ACCEPT = ".pdf,.docx,.txt";

export default function JdImportPanel({
  paste,
  onPasteChange,
  pasteMin,
  onExtractPaste,
  extracting,
  canExtractPaste,
  onUploadClick,
  uploading,
  error,
  fileInputRef,
  onFileChange,
}) {
  const pasteLen = paste.trim().length;

  return (
    <div className="jd-import-panel">
      <div className="jd-import-panel__head">
        <div className="jd-import-panel__intro">
          <h3 className="jd-import-panel__title">Import job description</h3>
          <p className="form-helper">
            Paste a full JD or upload a file — we&apos;ll pre-fill title, skills, compensation, and work setup when extraction succeeds.
          </p>
        </div>
      </div>

      <div className="jd-import-panel__upload-row">
        <input
          ref={fileInputRef}
          type="file"
          accept={ACCEPT}
          className="visually-hidden"
          id="jd-upload"
          onChange={(e) => onFileChange(e.target.files?.[0])}
        />
        <button
          type="button"
          className="jd-import-dropzone"
          onClick={onUploadClick}
          disabled={uploading || extracting}
        >
          <span className="jd-import-dropzone__label">Upload job description</span>
          <span className="jd-import-dropzone__hint">PDF, DOCX, or TXT · max 5 MB</span>
          <span className="jd-import-dropzone__action">
            {uploading ? "Parsing…" : "Choose file"}
          </span>
        </button>
      </div>

      <div className="jd-import-panel__or" aria-hidden="true">
        <span>or paste text</span>
      </div>

      <label className="jd-paste-field" htmlFor="jd-paste">
        <span className="jd-paste-field__label">Paste job description</span>
        <textarea
          id="jd-paste"
          className="jd-paste-field__textarea"
          rows={7}
          placeholder="Include title, responsibilities, required skills, experience, compensation, location, and employment type."
          value={paste}
          onChange={(e) => onPasteChange(e.target.value)}
          disabled={uploading}
        />
        <span className={`jd-paste-field__hint${pasteLen >= pasteMin ? " jd-paste-field__hint--ready" : ""}`}>
          {pasteLen > 0
            ? `${pasteLen.toLocaleString()} characters${pasteLen >= pasteMin ? " · ready to extract" : ` · ${pasteMin - pasteLen} more needed`}`
            : `At least ${pasteMin} characters to extract`}
        </span>
      </label>

      <div className="jd-import-panel__actions">
        <Button
          loading={extracting}
          loadingLabel="Extracting…"
          onClick={onExtractPaste}
          disabled={!canExtractPaste || uploading}
        >
          Extract details
        </Button>
        <p className="jd-import-panel__actions-hint form-helper">
          Review extracted fields below before posting. You can edit anything that looks off.
        </p>
      </div>

      {error && <p className="auth-error jd-import-error" role="alert">{error}</p>}
    </div>
  );
}
