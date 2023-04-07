import os
from tkinter import TclError
from tkinter import Tk
from tkinter import filedialog as fd

from langchain import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import UnstructuredWordDocumentLoader, UnstructuredPDFLoader, \
    UnstructuredEPubLoader, UnstructuredPowerPointLoader, UnstructuredFileLoader
from langchain.indexes import VectorstoreIndexCreator


def choose_a_doc() -> str:
    root = Tk()
    # credit to https://stackoverflow.com/a/54068050 for this trick
    try:
        try:
            root.tk.call('tk_getOpenFile', '-foobarbaz')
        except TclError:
            pass
        # now set the magic variables accordingly
        root.tk.call('set', '::tk::dialog::file::showHiddenBtn', '1')
        root.tk.call('set', '::tk::dialog::file::showHiddenVar', '0')
    except TclError:
        pass
    root.withdraw()
    return fd.askopenfilename(title="Select a document to talk to",
                              initialdir=os.path.expanduser("~"),
                              filetypes=(("PDF files", "*.pdf"), ("EPUB files", "*.epub"),
                                         ("Word files", "*.docx *.doc"), ("PowerPoint files", "*.pptx *.ppt")))


def select_loader_for_file(filename: str) -> UnstructuredFileLoader:
    try:
        loader = {
            ".doc": lambda f: UnstructuredWordDocumentLoader(f),
            ".docx": lambda f: UnstructuredWordDocumentLoader(f),
            ".pdf": lambda f: UnstructuredPDFLoader(f),
            ".epub": lambda f: UnstructuredEPubLoader(f),
            ".ppt": lambda f: UnstructuredPowerPointLoader(f),
            ".pptx": lambda f: UnstructuredPowerPointLoader(f),
        }[os.path.splitext(filename)[1]](filename)
        return loader
    except KeyError:
        print(f"File {filename} is of an unsupported file type.")
        exit(1)


def create_chain(loader: UnstructuredFileLoader) -> RetrievalQA:
    index_creator = VectorstoreIndexCreator()
    docsearch = index_creator.from_loaders([loader])

    chain = RetrievalQA.from_chain_type(
        llm=OpenAI(),
        chain_type="stuff",
        retriever=docsearch.vectorstore.as_retriever(),
        input_key="question",
    )
    return chain


def start_q_and_a(filename: str, chain: RetrievalQA):
    print(f"You're asking questions about '{os.path.split(filename)[1]}'.")
    print("Type your questions and press Enter. Press Ctrl + C to exit.")

    while True:
        try:
            query = input(f"{os.linesep}Question: ")
            sanitized_query = query.strip().replace(os.linesep, " ")
            response = chain({"question": sanitized_query})
            print(f"Answer: {response['result'].strip()}")
        except KeyboardInterrupt:
            print(f"{os.linesep}Goodbye!")
            break


if __name__ == "__main__":
    document_filename = choose_a_doc()
    document_loader = select_loader_for_file(document_filename)
    qa_chain = create_chain(document_loader)
    start_q_and_a(document_filename, qa_chain)
