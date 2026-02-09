"use client"; // Required because we use 'useState' (client-side logic)

import { useState } from "react";

export default function Home() {
  const [longUrl, setLongUrl] = useState("");
  const [shortUrl, setShortUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const handleShorten = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      // THE CONNECTION POINT: Sending data to our FastAPI backend
      const response = await fetch("http://localhost:8000/shorten", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: longUrl }),
      });

      const data = await response.json();
      setShortUrl(data.short_url);
    } catch (error) {
      console.error("Error connecting to backend:", error);
      alert("Make sure your Python backend is running on port 8000!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-black text-white flex flex-col items-center justify-center p-6">
      <div className="max-w-2xl w-full space-y-8 text-center">
        <h1 className="text-5xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400">
          ASCII URL Shortener
        </h1>
        <p className="text-gray-400">Paste your long link and get a tiny one back.</p>

        <form onSubmit={handleShorten} className="flex flex-col md:flex-row gap-3">
          <input
            type="url"
            required
            placeholder="https://example.com/very/long/path"
            className="flex-1 p-4 rounded-xl bg-gray-900 border border-gray-800 focus:border-blue-500 outline-none transition-all"
            value={longUrl}
            onChange={(e) => setLongUrl(e.target.value)}
          />
          <button
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-500 px-8 py-4 rounded-xl font-bold transition-all disabled:opacity-50"
          >
            {loading ? "Shortening..." : "Shorten IT"}
          </button>
        </form>

        {shortUrl && (
          <div className="p-6 bg-gray-900 border border-blue-500/30 rounded-2xl animate-in fade-in zoom-in duration-300">
            <p className="text-sm text-gray-400 mb-2">Success! Your short link is:</p>
            <div className="flex items-center justify-center gap-4">
              <a 
                href={shortUrl} 
                target="_blank" 
                className="text-2xl font-mono text-blue-400 hover:underline break-all"
              >
                {shortUrl}
              </a>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}