from src import parse

if __name__ == "__main__":
	parser = parse.setup_argparser()
	args = parser.parse_args()
	parse.main(args)