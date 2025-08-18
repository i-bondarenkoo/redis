from logging import getLogger, basicConfig, DEBUG


logger = getLogger()
FORMAT = "%(asctime)s : %(name)s : %(levelname)s : %(message)s"
basicConfig(level=DEBUG, format=FORMAT)
