type ModuleCardProps = {
  code: string;
  title: string;
  detail: string;
};

export function ModuleCard({ code, title, detail }: ModuleCardProps) {
  return (
    <article className="rounded-2xl border border-white/10 bg-white/5 p-5">
      <span className="inline-grid size-9 place-items-center rounded-lg bg-emerald-400/15 font-bold text-emerald-300">{code}</span>
      <h2 className="mt-4 font-semibold">{title}</h2>
      <p className="mt-2 text-sm leading-6 text-slate-400">{detail}</p>
    </article>
  );
}
