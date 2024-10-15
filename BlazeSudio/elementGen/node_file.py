from ast import literal_eval
import os.path
# Latest version OF THIS FILE TYPE, not of the actual BlazeSudios itself.
LATESTVER = [1, 0]

# TODO: Document this file format

class NodeFile:
    def __init__(self, allNodes, file=None):
        self.allNodes = allNodes
        if file is None or not os.path.exists(file):
            self.name = 'New File'
            self.conns = {}
            self.nodes = []
        else:
            with open(file, 'rb') as f:
                fc = f.read()
            dc = fc.decode()
            version = f'{fc[0]}.{fc[1]}'
            self.name = dc[2:fc.index(0, 2)]
            toprocess = fc[fc.index(0, 2)+1:]
            if version == '1.0':
                self._read_v1_0(toprocess)
            else:
                raise ValueError(
                    f'Version {self.version} is not supported!!'
                )
    
    def _read_v1_0(self, dat):
        self.nodes = []
        self.conns = {}
        
        infoBuilder = []
        escaped = False
        dataBuilder = b''
        conns = {}
        uids = {i.TypeHash(): i for i in self.allNodes}
        for i in range(len(dat)):
            b = dat[i:i+1]
            if b == b'\x00' and not escaped:
                infoBuilder.append(dataBuilder)
                dataBuilder = b''
            elif b == b'\x01' and not escaped:
                if infoBuilder == [] and dataBuilder == b'':
                    continue
                infoBuilder.append(dataBuilder)
                dataBuilder = b''
                if infoBuilder[0] == b'\x02':
                    n = uids[int(infoBuilder[1].decode())].copy()
                    idx = 4
                    for io in n.inputs+n.outputs:
                        nval = infoBuilder[idx].decode()
                        try:
                            io.value = literal_eval(nval)
                        except (ValueError, SyntaxError):
                            io.value = nval
                        idx += 1
                    self.nodes.append(((int(infoBuilder[2].decode()), int(infoBuilder[3].decode())), n))
                else:
                    conns[(int.from_bytes(infoBuilder[1]), int.from_bytes(infoBuilder[2]))] = \
                        (int.from_bytes(infoBuilder[3]), int.from_bytes(infoBuilder[4]))
                infoBuilder = []
            else:
                if escaped or b != b'\\':
                    dataBuilder += b
                    escaped = False
                else:
                    escaped = True
        
        for main, conn2 in conns.items():
            connFrom = self.nodes[main[0]][1]
            connTo = self.nodes[conn2[0]][1]
            self.conns[(connFrom, (connFrom.inputs+connFrom.outputs)[main[1]])] = \
                (connTo, (connTo.inputs+connTo.outputs)[conn2[1]])
    
    def _saveFile(self):
        def escapeBytes(b):
            return b.replace(b'\\', b'\\\\').replace(b'\x00', b'\\\x00').replace(b'\x01', b'\\\x01')
        dat = b''.join([int.to_bytes(i) for i in LATESTVER])
        dat += bytes(self.name, 'utf8') + b'\x00'
        if self.nodes == []:
            return dat
        for n in self.nodes:
            dat += b'\x02\x00' + escapeBytes(bytes(str(n[1].TypeHash()), 'utf8')) + b'\x00'
            dat += escapeBytes(bytes(str(n[0][0]), 'utf8')) + b'\x00' + escapeBytes(bytes(str(n[0][1]), 'utf8')) + b'\x00'
            for io in n[1].inputs+n[1].outputs:
                dat += escapeBytes(bytes(str(io.value), 'utf8')) + b'\x00'
            dat = dat[:-1]+b'\x01'
        vals = [i[1] for i in self.nodes]
        for main, conn in self.conns.items():
            dat += b'\x03\x00' + escapeBytes(int.to_bytes(vals.index(main[0]))) + b'\x00' + \
                escapeBytes(int.to_bytes((main[0].inputs+main[0].outputs).index(main[1]))) + b'\x00' + \
                escapeBytes(int.to_bytes(vals.index(conn[0]))) + b'\x00' + \
                escapeBytes(int.to_bytes((conn[0].inputs+conn[0].outputs).index(conn[1]))) + b'\x01'
        return dat
    
    def save(self, filepath):
        with open(filepath, 'wb+') as f:
            f.write(self._saveFile())
