import argparse, sqlite3, os, subprocess, sys
BASE=os.path.dirname(os.path.abspath(__file__))
DB=os.path.join(BASE,"tracker.db")
def conn():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
    c.execute("""CREATE TABLE IF NOT EXISTS visits(id INTEGER PRIMARY KEY AUTOINCREMENT, ip TEXT, ua TEXT, lat REAL, lon REAL, acc REAL, status TEXT, ts TEXT)""")
    c.commit(); return c
def cmd_list(args):
    c=conn()
    rows=c.execute("SELECT * FROM visits ORDER BY id DESC LIMIT ?",(args.limit,)).fetchall()
    if not rows: print("Belum ada data."); return
    for r in rows:
        loc = f"{r['lat']:.6f},{r['lon']:.6f}" if r['lat'] is not None else "-"
        acc = f"{r['acc']:.1f} m" if r['acc'] is not None else "-"
        print(f"#{r['id']} {r['ts']} | {r['status']} | ip={r['ip']} | loc={loc} | accuracy={acc}")
def cmd_serve(args):
    env=dict(os.environ); env["HOST"]=args.host; env["PORT"]=str(args.port)
    print(f"Serving on http://{args.host}:{args.port}")
    subprocess.run([sys.executable,"app.py"],cwd=BASE,env=env)
def cmd_clear(args):
    if input("Hapus semua data? (y/n) ")=="y":
        c=conn(); c.execute("DELETE FROM visits"); c.commit(); print("Dihapus.")
def cmd_stats(args):
    c=conn()
    total=c.execute("SELECT COUNT(*) FROM visits").fetchone()[0]
    allowed=c.execute("SELECT COUNT(*) FROM visits WHERE status='allowed'").fetchone()[0]
    print(f"total={total} allowed={allowed} denied={total-allowed}")
def main():
    p=argparse.ArgumentParser(prog="tracker",description="CLI tracker lokasi (demo lab)")
    sp=p.add_subparsers(dest="cmd",required=True)
    sp_list=sp.add_parser("list"); sp_list.add_argument("-n","--limit",type=int,default=50); sp_list.set_defaults(func=cmd_list)
    sp_serve=sp.add_parser("serve"); sp_serve.add_argument("--host",default="0.0.0.0"); sp_serve.add_argument("--port",type=int,default=5000); sp_serve.set_defaults(func=cmd_serve)
    sp_clear=sp.add_parser("clear"); sp_clear.set_defaults(func=cmd_clear)
    sp_stats=sp.add_parser("stats"); sp_stats.set_defaults(func=cmd_stats)
    args=p.parse_args(); args.func(args)
if __name__=="__main__":
    main()
