export const Header = () => {
  return (
    <header className="bg-gray-800 text-white p-4">
      <div className="container mx-auto">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">ابو سيف للتحميل بشكل مباشر</h1>
          <nav>
            <ul className="flex space-x-4">
              <li><a href="#" className="hover:text-gray-300">الرئيسية</a></li>
              <li><a href="#" className="hover:text-gray-300">الأقسام</a></li>
              <li><a href="#" className="hover:text-gray-300">أحدث الحلقات</a></li>
              <li><a href="#" className="hover:text-gray-300">أحدث الأفلام</a></li>
              <li><a href="#" className="hover:text-gray-300">أحدث المسلسلات</a></li>
            </ul>
          </nav>
        </div>
        <div className="mt-4">
          <input
            type="text"
            placeholder="ابحث عن فيلم أو مسلسل..."
            className="w-full p-2 rounded bg-gray-700 text-white"
          />
        </div>
      </div>
    </header>
  );
};
