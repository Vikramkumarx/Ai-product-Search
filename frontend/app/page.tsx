"use client";

import { useState, useEffect } from "react";
import axios from "axios";
import {
  Search, Sparkles, ShoppingBag, ArrowRight, MessagesSquare,
  Send, X, Bot, Star, Filter, Heart, Zap, ShieldCheck,
  Cpu, Layers, Laptop, Mail, Linkedin
} from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Slider } from "@/components/ui/slider";
import { Separator } from "@/components/ui/separator";
import { motion, AnimatePresence } from "framer-motion";

// --- TYPES ---
interface Product {
  product_id: number;
  product_name: string;
  category: string;
  price: number;
  rating: number;
  specifications: string;
  score?: number;
}

const API_URL = typeof window !== "undefined" && window.location.hostname !== "localhost"
  ? ""
  : (process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000");

const CATEGORIES = [
  { name: "All", icon: <Layers size={18} /> },
  { name: "Electronics", icon: <Cpu size={18} /> },
  { name: "Fashion", icon: <ShoppingBag size={18} /> },
  { name: "Groceries", icon: <Zap size={18} /> },
];

export default function Home() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);
  const [priceRange, setPriceRange] = useState([0, 300000]);
  const [debouncedQuery, setDebouncedQuery] = useState(query);
  const [activeCategory, setActiveCategory] = useState("All");

  // --- CHATBOT STATE ---
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [chatInput, setChatInput] = useState("");
  const [chatMessages, setChatMessages] = useState<any[]>([
    { role: 'bot', text: "Namaste! I'm your AI Product Expert. Need a recommendation or have questions about specs? Just ask!" }
  ]);
  const [isChatLoading, setIsChatLoading] = useState(false);

  // --- MODAL STATE ---
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);

  // --- DEBOUNCE SEARCH ---
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedQuery(query);
    }, 400);
    return () => clearTimeout(timer);
  }, [query]);

  useEffect(() => {
    if (debouncedQuery.length > 1) {
      handleSearch();
    } else if (debouncedQuery.length === 0) {
      setResults([]);
    }
  }, [debouncedQuery, activeCategory]);

  // --- API CALL ---
  const handleSearch = async () => {
    setLoading(true);
    try {
      const payload = {
        query: debouncedQuery,
        min_price: priceRange[0],
        max_price: priceRange[1],
        category: activeCategory
      };

      const res = await axios.post(`${API_URL}/search`, payload);
      setResults(res.data);
    } catch (err) {
      console.error("Search Error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async () => {
    if (!chatInput.trim()) return;

    const userMsg = { role: 'user', text: chatInput };
    setChatMessages(prev => [...prev, userMsg]);
    setChatInput("");
    setIsChatLoading(true);

    try {
      const res = await axios.post(`${API_URL}/chat`, { message: chatInput });
      const botMsg = { role: 'bot', text: res.data.response };
      setChatMessages(prev => [...prev, botMsg]);
    } catch (err) {
      console.error("Chat Error:", err);
      setChatMessages(prev => [...prev, { role: 'bot', text: "Apologies! My brain is a bit fuzzy right now. 😅" }]);
    } finally {
      setIsChatLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-50 text-slate-900 font-sans">

      {/* --- GLASS HEADER --- */}
      <header className="sticky top-0 z-50 glass border-b border-indigo-100/50 px-4 py-4 mb-8">
        <div className="max-w-7xl mx-auto flex items-center justify-between gap-6">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center gap-3"
          >
            <div className="h-10 w-10 bg-gradient-to-br from-indigo-600 to-violet-600 rounded-xl flex items-center justify-center text-white shadow-lg shadow-indigo-200">
              <Sparkles size={22} />
            </div>
            <h1 className="text-2xl font-black tracking-tight gradient-text">
              AI Expert
            </h1>
          </motion.div>

          <div className="flex-1 max-w-2xl relative group">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-indigo-500 transition-colors" size={20} />
            <Input
              className="w-full pl-12 h-12 bg-white/80 border-slate-200 rounded-full focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500 transition-all shadow-sm text-lg"
              placeholder="What are you looking for today?"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </div>

          <div className="hidden lg:flex items-center gap-3">
            <div className="h-10 w-10 rounded-full border border-slate-200 bg-white flex items-center justify-center text-slate-600">
              <Heart size={18} />
            </div>
            <div className="flex flex-col items-end">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-tighter">Premium User</span>
              <span className="text-sm font-bold text-slate-700">Vikram Kumar</span>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 grid grid-cols-1 lg:grid-cols-[280px_1fr] gap-10">

        {/* --- ADVANCED SIDEBAR --- */}
        <aside className="space-y-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white p-6 rounded-[2rem] border border-slate-100 shadow-xl shadow-slate-200/50"
          >
            <div className="flex items-center gap-2 mb-6">
              <Filter size={18} className="text-indigo-600" />
              <h3 className="font-bold text-lg text-slate-800">Curation Hub</h3>
            </div>

            <div className="space-y-2 mb-8">
              {CATEGORIES.map((cat) => (
                <button
                  key={cat.name}
                  onClick={() => { setActiveCategory(cat.name); if (query.length > 1) handleSearch(); }}
                  className={`w-full flex items-center justify-between px-4 py-3 rounded-2xl transition-all ${activeCategory === cat.name
                    ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-200'
                    : 'text-slate-500 hover:bg-slate-50 font-medium'
                    }`}
                >
                  <div className="flex items-center gap-3">
                    {cat.icon}
                    <span className="text-sm">{cat.name}</span>
                  </div>
                  {activeCategory === cat.name && <motion.div layoutId="activeCat" className="h-1.5 w-1.5 rounded-full bg-white" />}
                </button>
              ))}
            </div>

            <Separator className="bg-slate-100 my-6" />

            <div className="space-y-4">
              <label className="text-[10px] font-black uppercase text-slate-400 tracking-widest">Price Spectrum (₹)</label>
              <Slider
                value={priceRange}
                max={300000}
                step={1000}
                onValueChange={(val) => { setPriceRange(val); if (query.length > 1) handleSearch(); }}
                className="my-6"
              />
              <div className="flex justify-between items-center glass p-3 rounded-xl border-slate-100 shadow-inner">
                <span className="text-sm font-bold text-indigo-700">₹{priceRange[0].toLocaleString()}</span>
                <span className="text-sm font-bold text-indigo-700">₹{priceRange[1].toLocaleString()}</span>
              </div>
            </div>

            <div className="mt-8 p-4 bg-indigo-50 rounded-2xl border border-indigo-100">
              <div className="flex items-center gap-2 mb-2 text-indigo-700 font-bold text-[10px] uppercase">
                <ShieldCheck size={14} /> AI Verified result
              </div>
              <p className="text-[10px] text-indigo-600/70 leading-relaxed font-medium">
                Semantic vectors are used to match intent, not just keywords.
              </p>
            </div>
          </motion.div>
        </aside>

        {/* --- SEARCH RESULTS AREA --- */}
        <div className="min-h-[600px]">
          {query.length < 2 && results.length === 0 ? (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="h-full flex flex-col items-center justify-center p-12 text-center"
            >
              <div className="relative mb-8">
                <div className="absolute inset-0 bg-indigo-500/10 blur-[100px] rounded-full" />
                <ShoppingBag size={100} className="text-indigo-100 relative" />
                <motion.div
                  animate={{ y: [0, -10, 0] }}
                  transition={{ repeat: Infinity, duration: 2 }}
                  className="absolute -top-4 -right-4 h-16 w-16 bg-white rounded-2xl shadow-xl flex items-center justify-center text-3xl"
                >
                  🚀
                </motion.div>
              </div>
              <h2 className="text-4xl font-black text-slate-800 mb-4 tracking-tight">Discovery Engine</h2>
              <p className="text-lg text-slate-400 max-w-md mx-auto leading-relaxed font-medium">
                Search for anything — from "Gaming beasts" to "Premium watches".
                Our AI handles the complexity.
              </p>
            </motion.div>
          ) : (
            <div className="space-y-6">
              <div className="flex items-center justify-between px-2">
                <div>
                  <h2 className="text-2xl font-black text-slate-800"> Found {results.length} Elite Matches</h2>
                  <p className="text-sm text-slate-400 font-semibold tracking-tight">Ranked by AI precision and rating</p>
                </div>
                <div className="hidden sm:flex items-center gap-2 text-[10px] font-black text-slate-400 bg-white px-3 py-1.5 rounded-full border border-slate-100">
                  <span className="h-1.5 w-1.5 rounded-full bg-green-500 animate-pulse" /> Live Backend Connected
                </div>
              </div>

              <div className="grid grid-cols-1 gap-6">
                <AnimatePresence mode="popLayout">
                  {results.map((product, idx) => (
                    <motion.div
                      layout
                      initial={{ opacity: 0, y: 30 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, scale: 0.9 }}
                      transition={{ delay: idx * 0.05, duration: 0.4 }}
                      key={product.product_id}
                      className="group"
                    >
                      <Card className={`overflow-hidden border-none shadow-xl shadow-slate-200/50 rounded-[2.5rem] premium-card-hover transition-all duration-500 bg-white`}>
                        <div className="flex flex-col md:flex-row">

                          <div className="md:w-52 bg-slate-50 flex flex-col items-center justify-center p-8 relative overflow-hidden">
                            <motion.span
                              whileHover={{ rotate: 15, scale: 1.2 }}
                              className="text-7xl drop-shadow-2xl z-10"
                            >
                              {product.category === 'Electronics'
                                ? (product.product_name.toLowerCase().includes('watch') ? '⌚' : '💻')
                                : product.category === 'Fashion' ? '👕' : '📦'
                              }
                            </motion.span>
                            <div className="absolute inset-0 bg-indigo-500/5 rotate-12 translate-y-20 scale-150 group-hover:rotate-45 transition-transform duration-700" />
                          </div>

                          <div className="p-8 flex-1 flex flex-col justify-between">
                            <div>
                              <div className="flex items-center justify-between mb-4">
                                <div className="flex gap-2">
                                  <Badge variant="outline" className="rounded-full bg-white text-slate-500 border-slate-200 py-1 px-3 text-[10px] font-bold uppercase">
                                    {product.category}
                                  </Badge>
                                  {idx === 0 && (
                                    <Badge className="rounded-full bg-gradient-to-r from-indigo-600 to-violet-600 text-white border-none py-1 px-3 shadow-lg shadow-indigo-200 text-[10px] font-bold uppercase">
                                      <Sparkles size={12} className="mr-1" /> AI BEST CHOICE
                                    </Badge>
                                  )}
                                </div>
                                <div className="flex items-center gap-1.5 text-amber-500 bg-amber-50 px-3 py-1 rounded-full font-bold text-sm">
                                  <Star size={14} fill="currentColor" /> {product.rating}
                                </div>
                              </div>

                              <h3 className="text-2xl font-black text-slate-900 group-hover:text-indigo-600 transition-colors mb-2">
                                {product.product_name}
                              </h3>

                              <div className="flex flex-wrap gap-2 mt-4">
                                {product.specifications.split('|').slice(0, 4).map((spec, i) => (
                                  <span key={i} className="px-3 py-1.5 bg-slate-50 border border-slate-100 rounded-xl text-[10px] font-bold text-slate-500 uppercase tracking-tight">
                                    {spec.trim()}
                                  </span>
                                ))}
                              </div>
                            </div>

                            <div className="mt-8 pt-6 border-t border-slate-50 flex items-center justify-between">
                              <div>
                                <span className="text-[10px] font-black text-slate-400 uppercase tracking-wider block mb-1">Expert Price Point</span>
                                <span className="text-3xl font-black text-slate-900">₹{product.price.toLocaleString()}</span>
                              </div>
                              <Button
                                onClick={() => setSelectedProduct(product)}
                                className="h-14 px-8 rounded-2xl bg-indigo-600 hover:bg-indigo-700 text-white font-black shadow-xl shadow-indigo-200 flex items-center gap-2 group-hover:gap-4 transition-all"
                              >
                                Technical Specs <ArrowRight size={20} />
                              </Button>
                            </div>
                          </div>
                        </div>
                      </Card>
                    </motion.div>
                  ))}
                </AnimatePresence>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* --- PREMIUM AI CHATBOT --- */}
      <div className="fixed bottom-8 right-8 z-[100]">
        <AnimatePresence>
          {isChatOpen && (
            <motion.div
              initial={{ opacity: 0, scale: 0.8, y: 100 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.8, y: 100 }}
              className="bg-white/95 backdrop-blur-xl border border-white shadow-2xl rounded-[2.5rem] w-[380px] mb-6 overflow-hidden flex flex-col h-[550px]"
            >
              <div className="bg-gradient-to-r from-indigo-600 to-violet-700 p-6 text-white">
                <div className="flex justify-between items-center">
                  <div className="flex items-center gap-3">
                    <div className="h-10 w-10 bg-white/20 rounded-2xl flex items-center justify-center">
                      <Bot size={24} />
                    </div>
                    <div>
                      <p className="font-black text-lg">AI Assistant</p>
                      <div className="flex items-center gap-1.5">
                        <span className="h-2 w-2 rounded-full bg-green-400 animate-pulse" />
                        <span className="text-[10px] font-bold opacity-80 uppercase tracking-widest">Active Brain</span>
                      </div>
                    </div>
                  </div>
                  <button onClick={() => setIsChatOpen(false)} className="h-10 w-10 bg-white/10 hover:bg-white/20 rounded-2xl flex items-center justify-center transition-all">
                    <X size={24} />
                  </button>
                </div>
              </div>

              <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-hide">
                {chatMessages.map((msg, i) => (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    key={i}
                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div className={`max-w-[85%] p-4 rounded-[1.5rem] text-sm leading-relaxed ${msg.role === 'user'
                      ? 'bg-indigo-600 text-white rounded-tr-none shadow-xl shadow-indigo-100'
                      : 'bg-slate-100 text-slate-800 rounded-tl-none font-medium'
                      }`}>
                      {msg.text}
                    </div>
                  </motion.div>
                ))}
                {isChatLoading && (
                  <div className="flex justify-start">
                    <div className="bg-slate-100 p-4 rounded-3xl rounded-tl-none flex gap-1">
                      <span className="h-1.5 w-1.5 bg-slate-400 rounded-full animate-bounce" />
                      <span className="h-1.5 w-1.5 bg-slate-400 rounded-full animate-bounce [animation-delay:0.2s]" />
                      <span className="h-1.5 w-1.5 bg-slate-400 rounded-full animate-bounce [animation-delay:0.4s]" />
                    </div>
                  </div>
                )}
              </div>

              <div className="p-6 bg-white border-t border-slate-50 flex gap-3">
                <Input
                  placeholder="Ask me anything..."
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
                  className="rounded-2xl bg-slate-100 border-none h-14 font-medium"
                />
                <Button onClick={handleSendMessage} className="h-14 w-14 rounded-2xl bg-indigo-600 hover:bg-indigo-700 shadow-lg shadow-indigo-200 flex-shrink-0">
                  <Send size={24} />
                </Button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => setIsChatOpen(!isChatOpen)}
          className={`h-20 w-20 rounded-[2rem] shadow-2xl flex items-center justify-center transition-all duration-500 ${isChatOpen ? 'bg-slate-900 rotate-90' : 'bg-gradient-to-br from-indigo-600 to-violet-700'
            }`}
        >
          {isChatOpen ? <X size={32} className="text-white" /> : <MessagesSquare size={32} className="text-white" />}
        </motion.button>
      </div>

      {/* --- ULTIMATE SPECS OVERLAY --- */}
      <AnimatePresence>
        {selectedProduct && (
          <div className="fixed inset-0 z-[200] flex items-center justify-center p-4">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setSelectedProduct(null)}
              className="absolute inset-0 bg-slate-950/60 backdrop-blur-xl"
            />
            <motion.div
              initial={{ opacity: 0, scale: 0.9, y: 50 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.9, y: 50 }}
              className="bg-white rounded-[2.5rem] shadow-2xl w-full max-w-4xl overflow-hidden relative z-10"
            >
              <div className="grid grid-cols-1 lg:grid-cols-[1fr_400px] h-full">
                <div className="p-10 lg:p-14">
                  <div className="mb-8">
                    <Badge className="mb-4 bg-indigo-50 text-indigo-600 border-indigo-100 hover:bg-indigo-100 h-8 px-4 font-black uppercase text-[10px] tracking-widest">{selectedProduct.category}</Badge>
                    <h2 className="text-5xl font-black text-slate-900 leading-tight mb-2 tracking-tighter">{selectedProduct.product_name}</h2>
                    <div className="flex items-center gap-6">
                      <div className="flex items-center gap-2 text-amber-500 font-extrabold text-xl">
                        <Star size={24} fill="currentColor" /> {selectedProduct.rating}
                      </div>
                      <div className="h-8 w-[1px] bg-slate-100" />
                      <p className="text-slate-400 font-bold uppercase tracking-widest text-[10px]">Certified Product</p>
                    </div>
                  </div>

                  <div className="space-y-10">
                    <div>
                      <h4 className="font-black text-slate-900 mb-6 flex items-center gap-3">
                        <Zap size={22} className="text-indigo-600" />
                        Full Tech Specifications
                      </h4>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        {selectedProduct.specifications.split('|').map((spec, i) => (
                          <div key={i} className="flex items-start gap-4 p-5 bg-slate-50/50 border border-slate-100 rounded-2xl group hover:border-indigo-200 transition-colors">
                            <div className="mt-1.5 h-2 w-2 rounded-full bg-indigo-600 ring-4 ring-indigo-50 shadow-lg" />
                            <span className="text-sm font-bold text-slate-700 leading-relaxed tracking-tight">{spec.trim()}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-slate-50/80 p-10 lg:p-14 border-l border-slate-100 flex flex-col justify-between">
                  <div className="flex flex-col items-center">
                    <button
                      onClick={() => setSelectedProduct(null)}
                      className="self-end h-10 w-10 rounded-xl bg-white border border-slate-200 flex items-center justify-center hover:bg-slate-50 transition-all mb-8 shadow-sm"
                    >
                      <X size={24} />
                    </button>
                    <div className="h-64 w-64 bg-white rounded-[2.5rem] shadow-xl flex items-center justify-center text-9xl relative overflow-hidden">
                      <span className="relative z-10">
                        {selectedProduct.category === 'Electronics'
                          ? (selectedProduct.product_name.toLowerCase().includes('watch') ? '⌚' : '💻')
                          : selectedProduct.category === 'Fashion' ? '👕' : '📦'
                        }
                      </span>
                    </div>
                    <div className="text-center mt-10">
                      <p className="text-slate-400 font-bold uppercase tracking-widest text-[10px] mb-2">Price Point Experience</p>
                      <p className="text-6xl font-black text-slate-900 tracking-tighter">₹{selectedProduct.price.toLocaleString()}</p>
                    </div>
                  </div>

                  <div className="space-y-4">
                    <Button className="w-full h-16 text-xl font-black rounded-2xl shadow-2xl shadow-indigo-200 bg-indigo-600 hover:bg-indigo-700 group flex items-center justify-center gap-3">
                      Quick Purchase <ArrowRight size={24} className="group-hover:translate-x-1 transition-transform" />
                    </Button>
                    <div className="flex items-center justify-center gap-2 text-[10px] font-black uppercase text-slate-400 tracking-widest">
                      <ShieldCheck size={14} /> 100% Authentic Seller
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
      {/* --- PREMIUM FOOTER --- */}
      <footer className="mt-20 border-t border-slate-100 bg-white/50 backdrop-blur-sm pt-16 pb-12">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center gap-8">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 bg-gradient-to-br from-indigo-600 to-violet-600 rounded-xl flex items-center justify-center text-white shadow-lg">
                <Sparkles size={22} />
              </div>
              <div>
                <h3 className="text-lg font-black text-slate-900 leading-tight">AI Expert</h3>
                <p className="text-xs text-slate-400 font-bold uppercase tracking-widest">Next-Gen Search</p>
              </div>
            </div>

            <div className="flex flex-col items-center md:items-end gap-2">
              <div className="flex items-center gap-6">
                <a href="mailto:vikram10072003@gmail.com" className="h-10 w-10 rounded-full bg-indigo-50 flex items-center justify-center text-indigo-600 hover:bg-indigo-600 hover:text-white transition-all shadow-sm">
                  <Mail size={18} />
                </a>
                <a href="https://www.linkedin.com/in/vikram-kumar-51b9a1247" target="_blank" rel="noopener noreferrer" className="h-10 w-10 rounded-full bg-indigo-50 flex items-center justify-center text-indigo-600 hover:bg-indigo-600 hover:text-white transition-all shadow-sm">
                  <Linkedin size={18} />
                </a>
              </div>
              <div className="text-right">
                <p className="text-sm font-black text-slate-800">Designed & Developed by {activeCategory === "All" ? "Vikram Kumar" : "Vikram Kumar"}</p>
                <p className="text-xs text-slate-400 font-medium">Built with Next.js, FastAPI & Vector Search</p>
              </div>
            </div>
          </div>

          <Separator className="my-10 bg-slate-100" />

          <div className="flex flex-col sm:flex-row justify-between items-center gap-4 text-xs font-bold text-slate-400 uppercase tracking-widest">
            <p>© 2026 AI EXPERT. ALL RIGHTS RESERVED.</p>
            <div className="flex gap-8">
              <span className="hover:text-indigo-600 cursor-pointer transition-colors">Privacy Hub</span>
              <span className="hover:text-indigo-600 cursor-pointer transition-colors">Elite Terms</span>
            </div>
          </div>
        </div>
      </footer>
    </main>
  );
}
