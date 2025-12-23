export function UploadDropzone() {
  return (
    <section className="panel dropzone">
      <h3 className="dropzone__title">Upload screenshots or PDFs</h3>
      <p className="dropzone__hint">
        Drag files here to start extraction. Each file stays immutable with a
        hash in the audit log.
      </p>
      <div className="dropzone__actions">
        <label className="button">
          Select files
          <input type="file" multiple />
        </label>
        <span className="chip">PNG, JPG, PDF up to 20MB</span>
      </div>
    </section>
  );
}
