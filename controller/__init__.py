from . import add, asy, cd, clear, edit, index, nuke, paths, po, search, show, solve, status  # NOQA


class VonController:
	def do_ls(self, argv):
		self.do_cd(['.'] + argv)

	do_add = add.main
	do_asy = asy.main
	do_cd = cd.main
	do_clear = clear.main
	do_cs = do_cd
	do_edit = edit.main
	do_f = show.main  # alias find
	do_index = index.main
	do_nuke = nuke.main
	do_paths = paths.main
	do_po = po.main
	do_s = search.main
	do_search = search.main
	do_show = show.main
	do_solve = solve.main
	do_solve = solve.main
	do_ss = status.main
	do_status = status.main
