interface DownloadModalProps {
  isOpen: boolean;
  onClose: () => void;
  downloadLinks: { label: string; url: string }[];
}

export const DownloadModal = ({ isOpen, onClose, downloadLinks }: DownloadModalProps) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-gray-800 rounded-lg p-8 max-w-md w-full">
        <h2 className="text-2xl font-bold mb-4">روابط التحميل</h2>
        <ul className="space-y-4">
          {downloadLinks.map((link) => (
            <li key={link.url}>
              <a
                href={link.url}
                target="_blank"
                rel="noopener noreferrer"
                className="block bg-gray-700 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded"
              >
                {link.label}
              </a>
            </li>
          ))}
        </ul>
        <button
          onClick={onClose}
          className="mt-8 bg-red-500 hover:bg-red-400 text-white font-bold py-2 px-4 rounded"
        >
          إغلاق
        </button>
      </div>
    </div>
  );
};
