import { FileUploadZone } from "../FileUploadZone";

export default function FileUploadZoneExample() {
  return (
    <div className="p-8 max-w-3xl mx-auto">
      <FileUploadZone
        onFilesChange={(files) => console.log("Files uploaded:", files)}
      />
    </div>
  );
}
