// class FileSystem
// - rootFolder: Folder
//  create(): new folder or file
// delete(): deletes folder or file
// rename(): renames folder or file
// move(): moves folder or file
// list(path): show folder's contents
class FileSystem {
    constructor() {
        this.rootFolder = new Folder('')
    }
}

// class FileSystemEntry
// parent: FileSystemEntry
// children?: map<string, FileSystemEntry>
// name: string
//  createChild(): new folder or file
// deleteChild(): deletes folder or file
// rename(): renames folder or file
// getPath(): traverse up parents to root
// getChild(): return child

class FileSystemEntry {
    constructor(name) {
        this.children = new Map()
        this.name = name
    }

    createChild(name) {
        this.children.set(name, new FileSystemEntry(name))
    }
    listChildren(){
        for (let [name, child] of this.children.entries()) {
            console.log(child.name)
        }
    }
}

// class: Folder
// children?: map<string, FileSystemEntry[]>
class Folder extends FileSystemEntry {
    constructor(name) {
        super(name)
    }
}

// class: File
// content: string
// getContent(): return content
// setContent(): change content

class File extends FileSystemEntry {
    constructor(name) {
        super(name)
    }
}

const myFileSystem = new FileSystem()
const root = myFileSystem.rootFolder

root.createChild('file.txt')
root.listChildren()
console.log(root.children)