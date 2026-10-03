import React, {useEffect,useMemo,useState} from "react";
import {Routes,Route,NavLink,useNavigate,useLocation} from "react-router-dom";
import {LayoutDashboard,BookOpen,MessageCircle,ClipboardCheck,ChartNoAxesCombined,UserCircle,LogOut,Upload,BrainCircuit,Sparkles,ArrowRight,Clock3,Target,Menu,X,CheckCircle2,AlertCircle,Send,FileText,ChevronRight} from "lucide-react";
import api from "./api";

const nav=[["/","Dashboard",LayoutDashboard],["/materials","Materials",BookOpen],["/tutor","AI Tutor",MessageCircle],["/practice","Practice",ClipboardCheck],["/progress","My Progress",ChartNoAxesCombined],["/profile","Profile",UserCircle]];
const demo={name:"Student",overall_mastery:72,current_topic:"Deadlock Prevention",weak_topics:[{topic:"Deadlock Prevention",mastery:.42},{topic:"Synchronization",mastery:.56}],recommendations:[{title:"Review Deadlock Prevention",reason:"Estimated mastery is 42% and recent performance is below your target."},{title:"Practice 5 medium questions",reason:"Recent attempts show room to strengthen retrieval."},{title:"Review Synchronization",reason:"Mastery is developing; another focused pass is useful."}],recent:[70,80,60]};

function App(){
 const [user,setUser]=useState(()=>{try{return JSON.parse(localStorage.getItem("user"))}catch{return null}});
 const logout=()=>{localStorage.clear();setUser(null)};
 if(!user) return <Routes><Route path="*" element={<Auth onLogin={u=>setUser(u)}/>} /></Routes>;
 return <Shell user={user} logout={logout}/>;
}
function Shell({user,logout}){
 const [mobile,setMobile]=useState(false);
 return <div className="min-h-screen text-ink">
  <aside className={`fixed inset-y-0 left-0 z-30 w-64 border-r border-slate-200 bg-white/95 p-5 backdrop-blur transition-transform lg:translate-x-0 ${mobile?"translate-x-0":"-translate-x-full"}`}>
   <div className="mb-8 flex items-center gap-3"><div className="grid h-11 w-11 place-items-center rounded-2xl bg-indigo-600 text-white shadow-lg shadow-indigo-100"><BrainCircuit size={23}/></div><div><div className="font-extrabold tracking-tight">LearnFlow</div><div className="text-xs text-slate-400">Adaptive learning</div></div></div>
   <nav className="space-y-1">{nav.map(([to,label,Icon])=><NavLink onClick={()=>setMobile(false)} key={to} to={to} end={to==="/"} className={({isActive})=>`flex items-center gap-3 rounded-xl px-3 py-3 text-sm font-semibold ${isActive?"bg-indigo-50 text-indigo-700":"text-slate-500 hover:bg-slate-50 hover:text-slate-800"}`}><Icon size={18}/>{label}</NavLink>)}</nav>
   <div className="absolute bottom-5 left-5 right-5"><button onClick={logout} className="flex w-full items-center gap-3 rounded-xl px-3 py-3 text-sm font-semibold text-slate-500 hover:bg-red-50 hover:text-red-600"><LogOut size={18}/>Log out</button></div>
  </aside>
  {mobile&&<div onClick={()=>setMobile(false)} className="fixed inset-0 z-20 bg-slate-900/20 lg:hidden"/>}
  <main className="lg:pl-64"><header className="sticky top-0 z-10 flex h-16 items-center justify-between border-b border-slate-200/70 bg-white/80 px-4 backdrop-blur sm:px-8"><button className="lg:hidden" onClick={()=>setMobile(true)}><Menu/></button><div className="hidden text-sm text-slate-400 sm:block">Your personal learning space</div><div className="flex items-center gap-3"><div className="text-right"><div className="text-sm font-bold">{user.name}</div><div className="text-xs text-slate-400">{user.course||"Student"}</div></div><div className="grid h-9 w-9 place-items-center rounded-full bg-indigo-100 font-bold text-indigo-700">{(user.name||"S")[0]}</div></div></header><div className="mx-auto max-w-7xl p-4 sm:p-8"><Routes><Route path="/" element={<Dashboard/>}/><Route path="/materials" element={<Materials/>}/><Route path="/tutor" element={<Tutor/>}/><Route path="/practice" element={<Practice/>}/><Route path="/progress" element={<Progress/>}/><Route path="/profile" element={<Profile user={user}/>}/></Routes></div></main>
 </div>
}
function Auth({onLogin}){
 const [register,setRegister]=useState(false); const [form,setForm]=useState({name:"",email:"student@example.com",password:"student123",course:"Computer Science",semester:"6"}); const [err,setErr]=useState(""); const nav=useNavigate();
 async function submit(e){e.preventDefault();setErr("");try{const r=await api.post(register?"/auth/register":"/auth/login",form);localStorage.setItem("token",r.data.access_token);localStorage.setItem("user",JSON.stringify(r.data.student));onLogin(r.data.student);nav("/")}catch(e){setErr(e.response?.data?.detail||"Could not connect. Start the FastAPI backend.")}}
 return <div className="min-h-screen grid lg:grid-cols-2 bg-white"><div className="hidden lg:flex flex-col justify-between bg-indigo-600 p-12 text-white"><div><div className="flex items-center gap-3"><div className="grid h-12 w-12 place-items-center rounded-2xl bg-white/15"><BrainCircuit/></div><span className="text-xl font-extrabold">LearnFlow</span></div><div className="mt-24 max-w-lg"><p className="mb-4 text-sm font-semibold uppercase tracking-[.25em] text-indigo-200">Adaptive AI learning</p><h1 className="text-5xl font-black leading-tight">Study with a system that learns how you learn.</h1><p className="mt-6 text-lg leading-8 text-indigo-100">Materials, grounded tutoring, practice, mastery tracking and recommendations in one calm workspace.</p></div></div><div className="text-sm text-indigo-200">Learn · Practice · Analyze · Improve</div></div><div className="grid place-items-center p-6"><form onSubmit={submit} className="w-full max-w-md"><div className="mb-10 lg:hidden flex items-center gap-3"><div className="grid h-11 w-11 place-items-center rounded-2xl bg-indigo-600 text-white"><BrainCircuit/></div><b>LearnFlow</b></div><h2 className="text-3xl font-black">{register?"Create your account":"Welcome back"}</h2><p className="mt-2 text-slate-500">{register?"Set up your learning profile in a minute.":"Pick up where you left off."}</p>{err&&<div className="mt-5 rounded-xl bg-red-50 p-3 text-sm text-red-700">{err}</div>}<div className="mt-7 space-y-4">{register&&<input className="field" placeholder="Full name" value={form.name} onChange={e=>setForm({...form,name:e.target.value})} required/>}<input className="field" type="email" placeholder="Email" value={form.email} onChange={e=>setForm({...form,email:e.target.value})} required/><input className="field" type="password" placeholder="Password" value={form.password} onChange={e=>setForm({...form,password:e.target.value})} required/>{register&&<div className="grid grid-cols-2 gap-3"><input className="field" placeholder="Course / Branch" value={form.course} onChange={e=>setForm({...form,course:e.target.value})}/><input className="field" placeholder="Semester" value={form.semester} onChange={e=>setForm({...form,semester:e.target.value})}/></div>}<button className="btn-primary w-full">{register?"Create account":"Login"} <ArrowRight size={17}/></button></div><button type="button" onClick={()=>setRegister(!register)} className="mt-6 w-full text-center text-sm font-semibold text-indigo-600">{register?"Already have an account? Login":"Create account"}</button></form></div></div>
}
function Dashboard(){const [data,setData]=useState(demo);useEffect(()=>{api.get("/recommendations").then(r=>setData(d=>({...d,...r.data}))).catch(()=>{})},[]);return <><PageTitle eyebrow="DASHBOARD" title={`Welcome back 👋`} sub="Here is a clear picture of what to learn next."/><div className="grid gap-5 xl:grid-cols-3"><div className="card overflow-hidden bg-gradient-to-br from-indigo-600 to-violet-600 p-6 text-white xl:col-span-2"><div className="flex justify-between"><div><div className="text-sm font-semibold text-indigo-100">Continue learning</div><h2 className="mt-2 text-2xl font-black">{data.current_topic}</h2><p className="mt-2 text-sm text-indigo-100">Operating Systems · Mastery 42%</p></div><div className="rounded-2xl bg-white/15 p-3"><Target/></div></div><div className="mt-8 flex items-end justify-between"><div className="w-2/3"><div className="mb-2 h-2 rounded-full bg-white/20"><div className="h-2 rounded-full bg-white" style={{width:"42%"}}/></div><span className="text-xs text-indigo-100">Recommended next activity</span></div><button className="btn bg-white text-indigo-700">Continue <ArrowRight size={16}/></button></div></div><div className="card p-6"><div className="flex items-center justify-between"><span className="text-sm font-semibold text-slate-500">Overall mastery</span><Sparkles className="text-violet-500" size={20}/></div><div className="mt-4 text-5xl font-black">72<span className="text-2xl text-slate-400">%</span></div><p className="mt-2 text-sm text-slate-500">Across your tracked topics</p><div className="mt-5 h-2 rounded-full bg-slate-100"><div className="h-2 w-[72%] rounded-full bg-indigo-500"/></div></div></div><div className="mt-6 grid gap-5 lg:grid-cols-2"><section className="card p-6"><SectionHead title="Today's recommendations" icon={<Sparkles size={18}/>}/><div className="mt-4 space-y-3">{data.recommendations?.map((r,i)=><div key={i} className="rounded-xl bg-slate-50 p-4"><div className="flex items-center gap-3"><div className="grid h-8 w-8 place-items-center rounded-lg bg-white text-indigo-600 shadow-sm">{i+1}</div><b className="text-sm">{r.title}</b></div><p className="mt-2 pl-11 text-xs leading-5 text-slate-500">{r.reason}</p></div>)}</div></section><section className="card p-6"><SectionHead title="Recent activity" icon={<Clock3 size={18}/>}/><div className="mt-5 space-y-5">{data.recent.map((v,i)=><div key={i}><div className="mb-2 flex justify-between text-sm"><span>Quiz {i+1}</span><b>{v}%</b></div><div className="h-2 rounded-full bg-slate-100"><div className="h-2 rounded-full bg-indigo-500" style={{width:`${v}%`}}/></div></div>)}</div></section></div></>}
function Materials(){const [files,setFiles]=useState([]),[loading,setLoading]=useState(false),[msg,setMsg]=useState("");const upload=async e=>{const f=e.target.files[0];if(!f)return;setLoading(true);setMsg("Processing your material...");const fd=new FormData();fd.append("file",f);fd.append("subject","Operating Systems");try{const r=await api.post("/materials/upload",fd);setFiles(x=>[r.data,...x]);setMsg("Material processed successfully.");}catch(e){setMsg(e.response?.data?.detail||"Upload failed.")}finally{setLoading(false)}};useEffect(()=>{api.get("/materials").then(r=>setFiles(r.data)).catch(()=>{})},[]);return <><PageTitle eyebrow="MATERIALS" title="Your study library" sub="Upload class notes and let LearnFlow organize them into topics."/><div className="card mb-6 border-dashed p-8 text-center"><div className="mx-auto grid h-14 w-14 place-items-center rounded-2xl bg-indigo-50 text-indigo-600"><Upload/></div><h3 className="mt-4 text-lg font-bold">Add a study material</h3><p className="mt-1 text-sm text-slate-500">PDF, DOCX or TXT · up to 10 MB</p><label className="btn-primary mt-5 cursor-pointer">{loading?"Processing...":"Choose file"}<input hidden type="file" accept=".pdf,.docx,.txt" onChange={upload}/></label>{msg&&<p className="mt-4 text-sm text-slate-500">{msg}</p>}</div><div className="grid gap-4 md:grid-cols-2">{files.map(m=><div className="card p-5" key={m.id}><div className="flex gap-4"><div className="grid h-12 w-12 shrink-0 place-items-center rounded-xl bg-sky-50 text-sky-600"><FileText/></div><div className="min-w-0 flex-1"><h3 className="font-bold">{m.filename}</h3><p className="mt-1 text-xs text-slate-400">{m.subject||"Study material"} · {m.status||"processed"}</p><div className="mt-4 flex flex-wrap gap-2">{(m.topics||["Processes","CPU Scheduling","Synchronization","Deadlocks"]).map(t=><span className="pill bg-slate-100 text-slate-600" key={t}>{t}</span>)}</div><div className="mt-5 flex gap-2"><button className="btn-soft text-xs">Learn</button><button className="btn-soft text-xs">Summarize</button><button className="btn-soft text-xs">Practice</button></div></div></div></div>)}{!files.length&&<div className="card p-10 text-center md:col-span-2"><BookOpen className="mx-auto text-slate-300"/><p className="mt-3 font-semibold">No study material yet.</p><p className="mt-1 text-sm text-slate-500">Upload your first PDF to start learning.</p></div>}</div></>}
function Tutor(){const [q,setQ]=useState(""),[msgs,setMsgs]=useState([]),[loading,setLoading]=useState(false);async function ask(text=q){if(!text.trim())return;setMsgs(m=>[...m,{role:"user",text}]);setQ("");setLoading(true);try{const r=await api.post("/tutor/ask",{question:text});setMsgs(m=>[...m,{role:"assistant",text:r.data.answer,sources:r.data.sources,mode:r.data.mode}])}catch(e){setMsgs(m=>[...m,{role:"assistant",text:"I couldn't reach the tutor service. Start the backend and configure an LLM provider if you want live answers."}])}finally{setLoading(false)}}return <><PageTitle eyebrow="AI TUTOR" title="Ask your study assistant" sub="Answers are grounded in the study material available to your account."/><div className="card mx-auto flex min-h-[62vh] max-w-4xl flex-col overflow-hidden"><div className="border-b p-5"><div className="flex items-center gap-3"><div className="grid h-10 w-10 place-items-center rounded-xl bg-indigo-50 text-indigo-600"><BrainCircuit size={19}/></div><div><b>LearnFlow Tutor</b><p className="text-xs text-slate-400">RAG-grounded · context aware</p></div></div></div><div className="flex-1 space-y-5 overflow-auto p-5">{!msgs.length&&<div className="grid h-full place-items-center py-12 text-center"><div><div className="mx-auto grid h-16 w-16 place-items-center rounded-3xl bg-indigo-50 text-indigo-600"><MessageCircle/></div><h3 className="mt-4 text-xl font-bold">What are you learning today?</h3><p className="mt-2 text-sm text-slate-500">Try one of these</p><div className="mt-5 flex flex-wrap justify-center gap-2">{["Explain deadlock simply.","Give me an example.","Explain this for an exam.","Summarize this topic."].map(x=><button onClick={()=>ask(x)} className="btn-soft text-sm" key={x}>{x}</button>)}</div></div></div>}{msgs.map((m,i)=><div key={i} className={`flex ${m.role==="user"?"justify-end":""}`}><div className={`max-w-[85%] rounded-2xl p-4 text-sm leading-7 ${m.role==="user"?"bg-indigo-600 text-white":"bg-slate-50 text-slate-700"}`}>{m.text}{m.sources?.length>0&&<div className="mt-4 border-t border-slate-200 pt-3 text-xs text-slate-500"><b>Sources from your materials</b><div className="mt-2 space-y-1">{m.sources.map((s,j)=><div key={j}>• {s}</div>)}</div></div>}{m.mode==="demo"&&<div className="mt-3 text-[11px] font-semibold text-amber-600">Demo tutor mode</div>}</div></div>)}{loading&&<div className="text-sm text-slate-400">Thinking from your study material…</div>}</div><div className="border-t p-4"><div className="flex gap-2"><input className="field" value={q} onChange={e=>setQ(e.target.value)} onKeyDown={e=>e.key==="Enter"&&ask()} placeholder="Ask about your notes..."/><button onClick={()=>ask()} className="btn-primary px-4"><Send size={18}/></button></div><div className="mt-3 flex gap-2"><button className="text-xs font-semibold text-indigo-600" onClick={()=>ask("Explain simpler")}>Explain simpler</button><button className="text-xs font-semibold text-indigo-600" onClick={()=>ask("Give an example")}>Give example</button><button className="text-xs font-semibold text-indigo-600" onClick={()=>ask("Write an exam answer")}>Exam answer</button></div></div></div></>}
function Practice(){const [quiz,setQuiz]=useState(null),[answers,setAnswers]=useState({}),[result,setResult]=useState(null),[loading,setLoading]=useState(false);async function start(){setLoading(true);setResult(null);try{const r=await api.post("/quiz/generate",{subject:"Operating Systems",topic:"Deadlocks",number_of_questions:5,difficulty:"adaptive",question_type:"mcq"});setQuiz(r.data)}catch(e){setQuiz({id:"demo",questions:[{id:1,question:"Which condition is required for deadlock?",options:["Mutual exclusion","Compilation","Caching","Rendering"],correct_answer:"Mutual exclusion",explanation:"Mutual exclusion is one of the necessary Coffman conditions.",topic:"Deadlocks"}]})}finally{setLoading(false)}}async function submit(){try{const r=await api.post(`/quiz/${quiz.id}/submit`,{answers:Object.entries(answers).map(([question_id,answer])=>({question_id:Number(question_id),answer,time_taken:20}))});setResult(r.data)}catch{setResult({score:1,total:quiz.questions.length,percentage:100,correct:1,incorrect:0})}}return <><PageTitle eyebrow="PRACTICE" title="Practice that adapts to you" sub="Difficulty and topic selection can follow your mastery state."/><div className="grid gap-5 lg:grid-cols-3"><div className="card p-6 lg:col-span-1"><div className="pill w-fit bg-indigo-50 text-indigo-700">Recommended Practice</div><h2 className="mt-4 text-2xl font-black">Deadlocks</h2><p className="mt-2 text-sm text-slate-500">Adaptive difficulty · 5 questions</p><div className="mt-6 space-y-3 text-sm"><div className="flex justify-between"><span>Current mastery</span><b>42%</b></div><div className="h-2 rounded-full bg-slate-100"><div className="h-2 w-[42%] rounded-full bg-amber-400"/></div></div><button onClick={start} className="btn-primary mt-7 w-full">{loading?"Generating...":"Start practice"} <ArrowRight size={16}/></button></div><div className="card p-6 lg:col-span-2">{!quiz?<div className="grid min-h-[360px] place-items-center text-center"><ClipboardCheck className="text-slate-300" size={45}/><div><h3 className="mt-4 text-lg font-bold">Quick Practice</h3><p className="mt-1 text-sm text-slate-500">5 questions · Adaptive difficulty</p></div></div>:result?<div className="py-8 text-center"><CheckCircle2 className="mx-auto text-emerald-500" size={45}/><h2 className="mt-4 text-3xl font-black">{result.percentage}%</h2><p className="mt-2 text-slate-500">{result.correct} correct · {result.incorrect} incorrect</p><button onClick={start} className="btn-soft mt-6">Practice again</button></div>:<div><div className="mb-6 flex justify-between"><b>{quiz.questions.length} questions</b><span className="text-sm text-slate-400">Adaptive</span></div><div className="space-y-6">{quiz.questions.map((q,i)=><div key={q.id} className="rounded-2xl bg-slate-50 p-5"><p className="font-bold">{i+1}. {q.question}</p><div className="mt-4 grid gap-2">{q.options?.map(o=><label key={o} className={`flex cursor-pointer items-center gap-3 rounded-xl border bg-white p-3 text-sm ${answers[q.id]===o?"border-indigo-400 bg-indigo-50": "border-slate-200"}`}><input type="radio" name={`q${q.id}`} checked={answers[q.id]===o} onChange={()=>setAnswers(a=>({...a,[q.id]:o}))}/>{o}</label>)}</div></div>)}</div><button onClick={submit} className="btn-primary mt-6">Submit quiz</button></div>}</div></div></>}
function Progress() {
  const topics = [
    ["Processes", 91],
    ["Scheduling", 84],
    ["Synchronization", 56],
    ["Deadlocks", 38],
  ];

  return (
    <>
      <PageTitle
        eyebrow="MY PROGRESS"
        title="See how your knowledge is changing"
        sub="Your performance and mastery live in one place."
      />

      <div className="grid gap-5 lg:grid-cols-3">
        {/* Overall mastery */}
        <div className="card p-6 lg:col-span-1">
          <div className="text-sm text-slate-500">Overall mastery</div>

          <div className="mt-3 text-5xl font-black">72%</div>

          <div className="mt-5 h-3 rounded-full bg-slate-100">
            <div className="h-3 w-[72%] rounded-full bg-indigo-500" />
          </div>

          <p className="mt-5 text-sm leading-6 text-slate-500">
            Complete more targeted practice to update your knowledge state.
          </p>
        </div>

        {/* Topic mastery */}
        <div className="card p-6 lg:col-span-2">
          <SectionHead
            title="Topic mastery"
            icon={<Target size={18} />}
          />

          <div className="mt-5 space-y-5">
            {topics.map(([t, v]) => (
              <div key={t}>
                <div className="mb-2 flex justify-between text-sm">
                  <span className="font-semibold">{t}</span>
                  <b>{v}%</b>
                </div>

                <div className="h-2 rounded-full bg-slate-100">
                  <div
                    className={`h-2 rounded-full ${
                      v < 50
                        ? "bg-red-400"
                        : v < 70
                          ? "bg-amber-400"
                          : "bg-emerald-500"
                    }`}
                    style={{ width: `${v}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Performance */}
        <div className="card p-6 lg:col-span-2">
          <SectionHead
            title="Performance over time"
            icon={<ChartNoAxesCombined size={18} />}
          />

          <div className="mt-6 flex h-48 items-end gap-4">
            {[48, 62, 58, 75, 70, 84, 72].map((v, i) => (
              <div
                className="flex flex-1 flex-col items-center gap-2"
                key={i}
              >
                <div
                  className="w-full rounded-t-lg bg-indigo-100"
                  style={{ height: `${v * 1.7}px` }}
                />
                <span className="text-xs text-slate-400">
                  Q{i + 1}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Needs attention */}
        <div className="card p-6">
          <SectionHead
            title="Needs attention"
            icon={<AlertCircle size={18} />}
          />

          <div className="mt-5 rounded-xl bg-red-50 p-4">
            <b className="text-red-800">Deadlocks · 38%</b>

            <p className="mt-2 text-xs leading-5 text-red-700">
              Your recent performance suggests another focused review.
            </p>

            <button className="mt-3 text-xs font-bold text-red-700">
              Review now{" "}
              <ChevronRight className="inline" size={14} />
            </button>
          </div>

          <div className="mt-4 rounded-xl bg-amber-50 p-4">
            <b className="text-amber-800">
              Synchronization · 56%
            </b>

            <p className="mt-2 text-xs leading-5 text-amber-700">
              Practice a few medium questions.
            </p>
          </div>
        </div>
      </div>
    </>
  );
}
function Profile({user}){return <><PageTitle eyebrow="PROFILE" title="Your learning profile" sub="A simple place to review your account details."/><div className="card max-w-2xl p-6"><div className="flex items-center gap-4"><div className="grid h-16 w-16 place-items-center rounded-full bg-indigo-100 text-xl font-black text-indigo-700">{user.name?.[0]}</div><div><h2 className="text-xl font-black">{user.name}</h2><p className="text-sm text-slate-500">{user.email}</p></div></div><div className="mt-8 grid gap-4 sm:grid-cols-2"><Info label="Course / Branch" value={user.course||"Computer Science"}/><Info label="Semester" value={user.semester||"6"}/><Info label="Learning mode" value="Adaptive"/><Info label="DKT mode" value="Demo / configurable"/></div></div></>}
function Info({label,value}){return <div className="rounded-xl bg-slate-50 p-4"><div className="text-xs font-semibold uppercase tracking-wide text-slate-400">{label}</div><div className="mt-1 font-bold">{value}</div></div>}
function PageTitle({eyebrow,title,sub}){return <div className="mb-7"><div className="text-xs font-black tracking-[.2em] text-indigo-600">{eyebrow}</div><h1 className="mt-2 text-3xl font-black tracking-tight sm:text-4xl">{title}</h1><p className="mt-2 text-sm text-slate-500 sm:text-base">{sub}</p></div>}
function SectionHead({title,icon}){return <div className="flex items-center gap-2 text-slate-800"><span className="text-indigo-600">{icon}</span><h3 className="font-bold">{title}</h3></div>}
export default App;
