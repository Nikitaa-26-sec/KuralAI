
import Link from "next/link";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-[#080d18] text-white">
      <nav className="flex items-center justify-between px-8 py-6 md:px-16">
        <Link href="/" className="text-2xl font-bold tracking-tight">
          Kural<span className="text-teal-400">AI</span>
        </Link>

        <Link
          href="/chat"
          className="rounded-full bg-teal-400 px-6 py-3 font-semibold text-slate-950 transition hover:bg-teal-300"
        >
          Open Assistant
        </Link>
      </nav>

      <section className="mx-auto grid max-w-7xl items-center gap-12 px-8 py-24 md:grid-cols-2 md:px-16">
        <div>
          <p className="mb-5 text-sm font-semibold tracking-[0.25em] text-teal-400">
            HER VOICE. HER RIGHTS. HER KURAL.
          </p>

          <h1 className="text-5xl font-bold leading-tight md:text-7xl">
            Know your rights.
            <span className="block text-teal-400">
              Find your voice.
            </span>
          </h1>

          <p className="mt-7 max-w-xl text-lg leading-8 text-slate-300">
            KuralAI is a multilingual legal information assistant
            designed to make legal awareness easier to understand.
            Explore your rights, ask questions and learn about
            important reporting procedures.
          </p>

          <div className="mt-10 flex flex-wrap gap-4">
            <Link
              href="/chat"
              className="rounded-full bg-teal-400 px-8 py-4 font-semibold text-slate-950 hover:bg-teal-300"
            >
              Explore Legal Assistant →
            </Link>

            <Link
              href="/chat?mode=fir"
              className="rounded-full border border-slate-600 px-8 py-4 font-semibold hover:border-teal-400"
            >
              FIR Process Assistance
            </Link>
          </div>
        </div>

        <div className="rounded-3xl border border-slate-700 bg-slate-900/80 p-8 shadow-2xl">
          <p className="text-sm font-semibold tracking-widest text-teal-400">
            YOUR RIGHTS MATTER
          </p>

          <h2 className="mt-5 text-3xl font-bold">
            Legal awareness, made accessible.
          </h2>

          <p className="mt-4 leading-7 text-slate-400">
            Get clear information about workplace rights, legal
            protections and reporting procedures through a
            conversational assistant.
          </p>

          <div className="mt-8 space-y-4">
            <div className="rounded-xl border border-slate-700 p-5">
              <h3 className="font-semibold text-teal-300">
                Know Your Rights
              </h3>
              <p className="mt-2 text-sm text-slate-400">
                Explore legal information and workplace protections.
              </p>
            </div>

            <div className="rounded-xl border border-slate-700 p-5">
              <h3 className="font-semibold text-teal-300">
                Legal AI Assistant
              </h3>
              <p className="mt-2 text-sm text-slate-400">
                Ask questions and receive document-grounded responses.
              </p>
            </div>

            <div className="rounded-xl border border-slate-700 p-5">
              <h3 className="font-semibold text-teal-300">
                FIR Process Assistance
              </h3>
              <p className="mt-2 text-sm text-slate-400">
                Understand how to report incidents and find official
                reporting services.
              </p>
            </div>
          </div>
        </div>
      </section>

      <footer className="border-t border-slate-800 px-8 py-8 text-center text-sm text-slate-500">
        KuralAI © 2026 · Her voice. Her rights. Her Kural.
        <p className="mt-2">
          General legal information only. Not a substitute for
          professional legal advice.
        </p>
      </footer>
    </main>
  );
}
