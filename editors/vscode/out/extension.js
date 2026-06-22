"use strict";
var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name2 in all)
    __defProp(target, name2, { get: all[name2], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
  mod
));
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

// src/extension.ts
var extension_exports = {};
__export(extension_exports, {
  activate: () => activate,
  deactivate: () => deactivate
});
module.exports = __toCommonJS(extension_exports);
var vscode17 = __toESM(require("vscode"));

// src/core/catalog.ts
var vscode = __toESM(require("vscode"));
var CatalogManager = class {
  static {
    this.catalog = [];
  }
  static {
    this.OFFICIAL_URL = "https://raw.githubusercontent.com/wisrovi/wpipe-steps/001-DEVELOPMENT/steps_catalog.json";
  }
  static {
    this.COMMUNITY_URL = "https://raw.githubusercontent.com/wisrovi/wpipe-plugins/001-DEVELOPMENT/steps_catalog.json";
  }
  static async init(context) {
    const cacheUri = vscode.Uri.joinPath(context.globalStorageUri, "catalog_cache.json");
    try {
      const cacheData = await vscode.workspace.fs.readFile(cacheUri);
      const cached = JSON.parse(new TextDecoder().decode(cacheData));
      if (Array.isArray(cached)) this.catalog = cached;
    } catch (e) {
      try {
        const catalogUri = vscode.Uri.joinPath(context.extensionUri, "out", "steps_catalog.json");
        const catalogData = await vscode.workspace.fs.readFile(catalogUri);
        const raw = JSON.parse(new TextDecoder().decode(catalogData));
        this.catalog = Array.isArray(raw) ? raw : raw.default || [];
      } catch (e2) {
      }
    }
    this.update(context, false);
  }
  static async update(context, manual = false) {
    const download = async () => {
      const oldNames = new Set(this.catalog.map((s) => `${s.repo}:${s.name}`));
      const fetchJson = async (url, defaultRepo) => {
        try {
          const response = await fetch(url);
          if (!response.ok) return [];
          const p = await response.json();
          const items = Array.isArray(p) ? p : [];
          const baseUrl = url.substring(0, url.lastIndexOf("/") + 1);
          const resolveUrl = (path6) => {
            if (!path6) return void 0;
            if (path6.startsWith("http")) return path6;
            return `${baseUrl}${path6.startsWith("/") ? path6.substring(1) : path6}`;
          };
          return items.map((item) => ({
            ...item,
            repo: item.repo || defaultRepo,
            requirements: resolveUrl(item.requirements),
            examples: resolveUrl(item.examples)
          }));
        } catch (e) {
          return [];
        }
      };
      const [off, com] = await Promise.all([
        fetchJson(this.OFFICIAL_URL, "Official"),
        fetchJson(this.COMMUNITY_URL, "Community")
      ]);
      const newCatalog = [...off, ...com];
      if (newCatalog.length > 0) {
        const newItems = newCatalog.filter((s) => !oldNames.has(`${s.repo}:${s.name}`));
        this.catalog = newCatalog;
        try {
          const cacheUri = vscode.Uri.joinPath(context.globalStorageUri, "catalog_cache.json");
          await vscode.workspace.fs.writeFile(cacheUri, new TextEncoder().encode(JSON.stringify(this.catalog)));
        } catch (e) {
        }
        if (newItems.length > 0) {
          vscode.window.showInformationMessage(`\u{1F680} \xA1Hay ${newItems.length} nuevos estados en WPipe!`, "Ver Cat\xE1logo").then((selection) => {
            if (selection === "Ver Cat\xE1logo") vscode.commands.executeCommand("wpipe-vscode.searchSteps");
          });
        } else if (manual) {
          vscode.window.setStatusBarMessage("\u2705 WPipe: Cat\xE1logo al d\xEDa", 3e3);
        }
        vscode.commands.executeCommand("wpipeSteps.refreshEntry");
      }
    };
    if (manual) {
      await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "Actualizando cat\xE1logo...",
        cancellable: false
      }, download);
    } else {
      download();
    }
  }
  static getSteps() {
    return this.catalog;
  }
};

// src/providers/stepProvider.ts
var vscode3 = __toESM(require("vscode"));

// src/core/workspaceIndex.ts
var vscode2 = __toESM(require("vscode"));

// node_modules/@lezer/common/dist/index.js
var DefaultBufferLength = 1024;
var nextPropID = 0;
var Range = class {
  constructor(from, to) {
    this.from = from;
    this.to = to;
  }
};
var NodeProp = class {
  /**
  Create a new node prop type.
  */
  constructor(config = {}) {
    this.id = nextPropID++;
    this.perNode = !!config.perNode;
    this.deserialize = config.deserialize || (() => {
      throw new Error("This node type doesn't define a deserialize function");
    });
    this.combine = config.combine || null;
  }
  /**
  This is meant to be used with
  [`NodeSet.extend`](#common.NodeSet.extend) or
  [`LRParser.configure`](#lr.ParserConfig.props) to compute
  prop values for each node type in the set. Takes a [match
  object](#common.NodeType^match) or function that returns undefined
  if the node type doesn't get this prop, and the prop's value if
  it does.
  */
  add(match) {
    if (this.perNode)
      throw new RangeError("Can't add per-node props to node types");
    if (typeof match != "function")
      match = NodeType.match(match);
    return (type) => {
      let result = match(type);
      return result === void 0 ? null : [this, result];
    };
  }
};
NodeProp.closedBy = new NodeProp({ deserialize: (str) => str.split(" ") });
NodeProp.openedBy = new NodeProp({ deserialize: (str) => str.split(" ") });
NodeProp.group = new NodeProp({ deserialize: (str) => str.split(" ") });
NodeProp.isolate = new NodeProp({ deserialize: (value) => {
  if (value && value != "rtl" && value != "ltr" && value != "auto")
    throw new RangeError("Invalid value for isolate: " + value);
  return value || "auto";
} });
NodeProp.contextHash = new NodeProp({ perNode: true });
NodeProp.lookAhead = new NodeProp({ perNode: true });
NodeProp.mounted = new NodeProp({ perNode: true });
var MountedTree = class {
  constructor(tree, overlay, parser2, bracketed2 = false) {
    this.tree = tree;
    this.overlay = overlay;
    this.parser = parser2;
    this.bracketed = bracketed2;
  }
  /**
  @internal
  */
  static get(tree) {
    return tree && tree.props && tree.props[NodeProp.mounted.id];
  }
};
var noProps = /* @__PURE__ */ Object.create(null);
var NodeType = class _NodeType {
  /**
  @internal
  */
  constructor(name2, props, id2, flags = 0) {
    this.name = name2;
    this.props = props;
    this.id = id2;
    this.flags = flags;
  }
  /**
  Define a node type.
  */
  static define(spec) {
    let props = spec.props && spec.props.length ? /* @__PURE__ */ Object.create(null) : noProps;
    let flags = (spec.top ? 1 : 0) | (spec.skipped ? 2 : 0) | (spec.error ? 4 : 0) | (spec.name == null ? 8 : 0);
    let type = new _NodeType(spec.name || "", props, spec.id, flags);
    if (spec.props)
      for (let src of spec.props) {
        if (!Array.isArray(src))
          src = src(type);
        if (src) {
          if (src[0].perNode)
            throw new RangeError("Can't store a per-node prop on a node type");
          props[src[0].id] = src[1];
        }
      }
    return type;
  }
  /**
  Retrieves a node prop for this type. Will return `undefined` if
  the prop isn't present on this node.
  */
  prop(prop) {
    return this.props[prop.id];
  }
  /**
  True when this is the top node of a grammar.
  */
  get isTop() {
    return (this.flags & 1) > 0;
  }
  /**
  True when this node is produced by a skip rule.
  */
  get isSkipped() {
    return (this.flags & 2) > 0;
  }
  /**
  Indicates whether this is an error node.
  */
  get isError() {
    return (this.flags & 4) > 0;
  }
  /**
  When true, this node type doesn't correspond to a user-declared
  named node, for example because it is used to cache repetition.
  */
  get isAnonymous() {
    return (this.flags & 8) > 0;
  }
  /**
  Returns true when this node's name or one of its
  [groups](#common.NodeProp^group) matches the given string.
  */
  is(name2) {
    if (typeof name2 == "string") {
      if (this.name == name2)
        return true;
      let group = this.prop(NodeProp.group);
      return group ? group.indexOf(name2) > -1 : false;
    }
    return this.id == name2;
  }
  /**
  Create a function from node types to arbitrary values by
  specifying an object whose property names are node or
  [group](#common.NodeProp^group) names. Often useful with
  [`NodeProp.add`](#common.NodeProp.add). You can put multiple
  names, separated by spaces, in a single property name to map
  multiple node names to a single value.
  */
  static match(map) {
    let direct = /* @__PURE__ */ Object.create(null);
    for (let prop in map)
      for (let name2 of prop.split(" "))
        direct[name2] = map[prop];
    return (node) => {
      for (let groups = node.prop(NodeProp.group), i = -1; i < (groups ? groups.length : 0); i++) {
        let found = direct[i < 0 ? node.name : groups[i]];
        if (found)
          return found;
      }
    };
  }
};
NodeType.none = new NodeType(
  "",
  /* @__PURE__ */ Object.create(null),
  0,
  8
  /* NodeFlag.Anonymous */
);
var NodeSet = class _NodeSet {
  /**
  Create a set with the given types. The `id` property of each
  type should correspond to its position within the array.
  */
  constructor(types) {
    this.types = types;
    for (let i = 0; i < types.length; i++)
      if (types[i].id != i)
        throw new RangeError("Node type ids should correspond to array positions when creating a node set");
  }
  /**
  Create a copy of this set with some node properties added. The
  arguments to this method can be created with
  [`NodeProp.add`](#common.NodeProp.add).
  */
  extend(...props) {
    let newTypes = [];
    for (let type of this.types) {
      let newProps = null;
      for (let source of props) {
        let add = source(type);
        if (add) {
          if (!newProps)
            newProps = Object.assign({}, type.props);
          let value = add[1], prop = add[0];
          if (prop.combine && prop.id in newProps)
            value = prop.combine(newProps[prop.id], value);
          newProps[prop.id] = value;
        }
      }
      newTypes.push(newProps ? new NodeType(type.name, newProps, type.id, type.flags) : type);
    }
    return new _NodeSet(newTypes);
  }
};
var CachedNode = /* @__PURE__ */ new WeakMap();
var CachedInnerNode = /* @__PURE__ */ new WeakMap();
var IterMode;
(function(IterMode2) {
  IterMode2[IterMode2["ExcludeBuffers"] = 1] = "ExcludeBuffers";
  IterMode2[IterMode2["IncludeAnonymous"] = 2] = "IncludeAnonymous";
  IterMode2[IterMode2["IgnoreMounts"] = 4] = "IgnoreMounts";
  IterMode2[IterMode2["IgnoreOverlays"] = 8] = "IgnoreOverlays";
  IterMode2[IterMode2["EnterBracketed"] = 16] = "EnterBracketed";
})(IterMode || (IterMode = {}));
var Tree = class _Tree {
  /**
  Construct a new tree. See also [`Tree.build`](#common.Tree^build).
  */
  constructor(type, children, positions, length, props) {
    this.type = type;
    this.children = children;
    this.positions = positions;
    this.length = length;
    this.props = null;
    if (props && props.length) {
      this.props = /* @__PURE__ */ Object.create(null);
      for (let [prop, value] of props)
        this.props[typeof prop == "number" ? prop : prop.id] = value;
    }
  }
  /**
  @internal
  */
  toString() {
    let mounted = MountedTree.get(this);
    if (mounted && !mounted.overlay)
      return mounted.tree.toString();
    let children = "";
    for (let ch of this.children) {
      let str = ch.toString();
      if (str) {
        if (children)
          children += ",";
        children += str;
      }
    }
    return !this.type.name ? children : (/\W/.test(this.type.name) && !this.type.isError ? JSON.stringify(this.type.name) : this.type.name) + (children.length ? "(" + children + ")" : "");
  }
  /**
  Get a [tree cursor](#common.TreeCursor) positioned at the top of
  the tree. Mode can be used to [control](#common.IterMode) which
  nodes the cursor visits.
  */
  cursor(mode = 0) {
    return new TreeCursor(this.topNode, mode);
  }
  /**
  Get a [tree cursor](#common.TreeCursor) pointing into this tree
  at the given position and side (see
  [`moveTo`](#common.TreeCursor.moveTo).
  */
  cursorAt(pos, side = 0, mode = 0) {
    let scope = CachedNode.get(this) || this.topNode;
    let cursor = new TreeCursor(scope);
    cursor.moveTo(pos, side);
    CachedNode.set(this, cursor._tree);
    return cursor;
  }
  /**
  Get a [syntax node](#common.SyntaxNode) object for the top of the
  tree.
  */
  get topNode() {
    return new TreeNode(this, 0, 0, null);
  }
  /**
  Get the [syntax node](#common.SyntaxNode) at the given position.
  If `side` is -1, this will move into nodes that end at the
  position. If 1, it'll move into nodes that start at the
  position. With 0, it'll only enter nodes that cover the position
  from both sides.
  
  Note that this will not enter
  [overlays](#common.MountedTree.overlay), and you often want
  [`resolveInner`](#common.Tree.resolveInner) instead.
  */
  resolve(pos, side = 0) {
    let node = resolveNode(CachedNode.get(this) || this.topNode, pos, side, false);
    CachedNode.set(this, node);
    return node;
  }
  /**
  Like [`resolve`](#common.Tree.resolve), but will enter
  [overlaid](#common.MountedTree.overlay) nodes, producing a syntax node
  pointing into the innermost overlaid tree at the given position
  (with parent links going through all parent structure, including
  the host trees).
  */
  resolveInner(pos, side = 0) {
    let node = resolveNode(CachedInnerNode.get(this) || this.topNode, pos, side, true);
    CachedInnerNode.set(this, node);
    return node;
  }
  /**
  In some situations, it can be useful to iterate through all
  nodes around a position, including those in overlays that don't
  directly cover the position. This method gives you an iterator
  that will produce all nodes, from small to big, around the given
  position.
  */
  resolveStack(pos, side = 0) {
    return stackIterator(this, pos, side);
  }
  /**
  Iterate over the tree and its children, calling `enter` for any
  node that touches the `from`/`to` region (if given) before
  running over such a node's children, and `leave` (if given) when
  leaving the node. When `enter` returns `false`, that node will
  not have its children iterated over (or `leave` called).
  */
  iterate(spec) {
    let { enter, leave, from = 0, to = this.length } = spec;
    let mode = spec.mode || 0, anon = (mode & IterMode.IncludeAnonymous) > 0;
    for (let c = this.cursor(mode | IterMode.IncludeAnonymous); ; ) {
      let entered = false;
      if (c.from <= to && c.to >= from && (!anon && c.type.isAnonymous || enter(c) !== false)) {
        if (c.firstChild())
          continue;
        entered = true;
      }
      for (; ; ) {
        if (entered && leave && (anon || !c.type.isAnonymous))
          leave(c);
        if (c.nextSibling())
          break;
        if (!c.parent())
          return;
        entered = true;
      }
    }
  }
  /**
  Get the value of the given [node prop](#common.NodeProp) for this
  node. Works with both per-node and per-type props.
  */
  prop(prop) {
    return !prop.perNode ? this.type.prop(prop) : this.props ? this.props[prop.id] : void 0;
  }
  /**
  Returns the node's [per-node props](#common.NodeProp.perNode) in a
  format that can be passed to the [`Tree`](#common.Tree)
  constructor.
  */
  get propValues() {
    let result = [];
    if (this.props)
      for (let id2 in this.props)
        result.push([+id2, this.props[id2]]);
    return result;
  }
  /**
  Balance the direct children of this tree, producing a copy of
  which may have children grouped into subtrees with type
  [`NodeType.none`](#common.NodeType^none).
  */
  balance(config = {}) {
    return this.children.length <= 8 ? this : balanceRange(NodeType.none, this.children, this.positions, 0, this.children.length, 0, this.length, (children, positions, length) => new _Tree(this.type, children, positions, length, this.propValues), config.makeTree || ((children, positions, length) => new _Tree(NodeType.none, children, positions, length)));
  }
  /**
  Build a tree from a postfix-ordered buffer of node information,
  or a cursor over such a buffer.
  */
  static build(data) {
    return buildTree(data);
  }
};
Tree.empty = new Tree(NodeType.none, [], [], 0);
var FlatBufferCursor = class _FlatBufferCursor {
  constructor(buffer, index) {
    this.buffer = buffer;
    this.index = index;
  }
  get id() {
    return this.buffer[this.index - 4];
  }
  get start() {
    return this.buffer[this.index - 3];
  }
  get end() {
    return this.buffer[this.index - 2];
  }
  get size() {
    return this.buffer[this.index - 1];
  }
  get pos() {
    return this.index;
  }
  next() {
    this.index -= 4;
  }
  fork() {
    return new _FlatBufferCursor(this.buffer, this.index);
  }
};
var TreeBuffer = class _TreeBuffer {
  /**
  Create a tree buffer.
  */
  constructor(buffer, length, set) {
    this.buffer = buffer;
    this.length = length;
    this.set = set;
  }
  /**
  @internal
  */
  get type() {
    return NodeType.none;
  }
  /**
  @internal
  */
  toString() {
    let result = [];
    for (let index = 0; index < this.buffer.length; ) {
      result.push(this.childString(index));
      index = this.buffer[index + 3];
    }
    return result.join(",");
  }
  /**
  @internal
  */
  childString(index) {
    let id2 = this.buffer[index], endIndex = this.buffer[index + 3];
    let type = this.set.types[id2], result = type.name;
    if (/\W/.test(result) && !type.isError)
      result = JSON.stringify(result);
    index += 4;
    if (endIndex == index)
      return result;
    let children = [];
    while (index < endIndex) {
      children.push(this.childString(index));
      index = this.buffer[index + 3];
    }
    return result + "(" + children.join(",") + ")";
  }
  /**
  @internal
  */
  findChild(startIndex, endIndex, dir, pos, side) {
    let { buffer } = this, pick = -1;
    for (let i = startIndex; i != endIndex; i = buffer[i + 3]) {
      if (checkSide(side, pos, buffer[i + 1], buffer[i + 2])) {
        pick = i;
        if (dir > 0)
          break;
      }
    }
    return pick;
  }
  /**
  @internal
  */
  slice(startI, endI, from) {
    let b = this.buffer;
    let copy = new Uint16Array(endI - startI), len = 0;
    for (let i = startI, j = 0; i < endI; ) {
      copy[j++] = b[i++];
      copy[j++] = b[i++] - from;
      let to = copy[j++] = b[i++] - from;
      copy[j++] = b[i++] - startI;
      len = Math.max(len, to);
    }
    return new _TreeBuffer(copy, len, this.set);
  }
};
function checkSide(side, pos, from, to) {
  switch (side) {
    case -2:
      return from < pos;
    case -1:
      return to >= pos && from < pos;
    case 0:
      return from < pos && to > pos;
    case 1:
      return from <= pos && to > pos;
    case 2:
      return to > pos;
    case 4:
      return true;
  }
}
function resolveNode(node, pos, side, overlays) {
  var _a;
  while (node.from == node.to || (side < 1 ? node.from >= pos : node.from > pos) || (side > -1 ? node.to <= pos : node.to < pos)) {
    let parent = !overlays && node instanceof TreeNode && node.index < 0 ? null : node.parent;
    if (!parent)
      return node;
    node = parent;
  }
  let mode = overlays ? 0 : IterMode.IgnoreOverlays;
  if (overlays)
    for (let scan = node, parent = scan.parent; parent; scan = parent, parent = scan.parent) {
      if (scan instanceof TreeNode && scan.index < 0 && ((_a = parent.enter(pos, side, mode)) === null || _a === void 0 ? void 0 : _a.from) != scan.from)
        node = parent;
    }
  for (; ; ) {
    let inner = node.enter(pos, side, mode);
    if (!inner)
      return node;
    node = inner;
  }
}
var BaseNode = class {
  cursor(mode = 0) {
    return new TreeCursor(this, mode);
  }
  getChild(type, before = null, after = null) {
    let r = getChildren(this, type, before, after);
    return r.length ? r[0] : null;
  }
  getChildren(type, before = null, after = null) {
    return getChildren(this, type, before, after);
  }
  resolve(pos, side = 0) {
    return resolveNode(this, pos, side, false);
  }
  resolveInner(pos, side = 0) {
    return resolveNode(this, pos, side, true);
  }
  matchContext(context) {
    return matchNodeContext(this.parent, context);
  }
  enterUnfinishedNodesBefore(pos) {
    let scan = this.childBefore(pos), node = this;
    while (scan) {
      let last = scan.lastChild;
      if (!last || last.to != scan.to)
        break;
      if (last.type.isError && last.from == last.to) {
        node = scan;
        scan = last.prevSibling;
      } else {
        scan = last;
      }
    }
    return node;
  }
  get node() {
    return this;
  }
  get next() {
    return this.parent;
  }
};
var TreeNode = class _TreeNode extends BaseNode {
  constructor(_tree, from, index, _parent) {
    super();
    this._tree = _tree;
    this.from = from;
    this.index = index;
    this._parent = _parent;
  }
  get type() {
    return this._tree.type;
  }
  get name() {
    return this._tree.type.name;
  }
  get to() {
    return this.from + this._tree.length;
  }
  nextChild(i, dir, pos, side, mode = 0) {
    for (let parent = this; ; ) {
      for (let { children, positions } = parent._tree, e = dir > 0 ? children.length : -1; i != e; i += dir) {
        let next = children[i], start = positions[i] + parent.from, mounted;
        if (!(mode & IterMode.EnterBracketed && next instanceof Tree && (mounted = MountedTree.get(next)) && !mounted.overlay && mounted.bracketed && pos >= start && pos <= start + next.length) && !checkSide(side, pos, start, start + next.length))
          continue;
        if (next instanceof TreeBuffer) {
          if (mode & IterMode.ExcludeBuffers)
            continue;
          let index = next.findChild(0, next.buffer.length, dir, pos - start, side);
          if (index > -1)
            return new BufferNode(new BufferContext(parent, next, i, start), null, index);
        } else if (mode & IterMode.IncludeAnonymous || (!next.type.isAnonymous || hasChild(next))) {
          let mounted2;
          if (!(mode & IterMode.IgnoreMounts) && (mounted2 = MountedTree.get(next)) && !mounted2.overlay)
            return new _TreeNode(mounted2.tree, start, i, parent);
          let inner = new _TreeNode(next, start, i, parent);
          return mode & IterMode.IncludeAnonymous || !inner.type.isAnonymous ? inner : inner.nextChild(dir < 0 ? next.children.length - 1 : 0, dir, pos, side, mode);
        }
      }
      if (mode & IterMode.IncludeAnonymous || !parent.type.isAnonymous)
        return null;
      if (parent.index >= 0)
        i = parent.index + dir;
      else
        i = dir < 0 ? -1 : parent._parent._tree.children.length;
      parent = parent._parent;
      if (!parent)
        return null;
    }
  }
  get firstChild() {
    return this.nextChild(
      0,
      1,
      0,
      4
      /* Side.DontCare */
    );
  }
  get lastChild() {
    return this.nextChild(
      this._tree.children.length - 1,
      -1,
      0,
      4
      /* Side.DontCare */
    );
  }
  childAfter(pos) {
    return this.nextChild(
      0,
      1,
      pos,
      2
      /* Side.After */
    );
  }
  childBefore(pos) {
    return this.nextChild(
      this._tree.children.length - 1,
      -1,
      pos,
      -2
      /* Side.Before */
    );
  }
  prop(prop) {
    return this._tree.prop(prop);
  }
  enter(pos, side, mode = 0) {
    let mounted;
    if (!(mode & IterMode.IgnoreOverlays) && (mounted = MountedTree.get(this._tree)) && mounted.overlay) {
      let rPos = pos - this.from, enterBracketed = mode & IterMode.EnterBracketed && mounted.bracketed;
      for (let { from, to } of mounted.overlay) {
        if ((side > 0 || enterBracketed ? from <= rPos : from < rPos) && (side < 0 || enterBracketed ? to >= rPos : to > rPos))
          return new _TreeNode(mounted.tree, mounted.overlay[0].from + this.from, -1, this);
      }
    }
    return this.nextChild(0, 1, pos, side, mode);
  }
  nextSignificantParent() {
    let val = this;
    while (val.type.isAnonymous && val._parent)
      val = val._parent;
    return val;
  }
  get parent() {
    return this._parent ? this._parent.nextSignificantParent() : null;
  }
  get nextSibling() {
    return this._parent && this.index >= 0 ? this._parent.nextChild(
      this.index + 1,
      1,
      0,
      4
      /* Side.DontCare */
    ) : null;
  }
  get prevSibling() {
    return this._parent && this.index >= 0 ? this._parent.nextChild(
      this.index - 1,
      -1,
      0,
      4
      /* Side.DontCare */
    ) : null;
  }
  get tree() {
    return this._tree;
  }
  toTree() {
    return this._tree;
  }
  /**
  @internal
  */
  toString() {
    return this._tree.toString();
  }
};
function getChildren(node, type, before, after) {
  let cur = node.cursor(), result = [];
  if (!cur.firstChild())
    return result;
  if (before != null)
    for (let found = false; !found; ) {
      found = cur.type.is(before);
      if (!cur.nextSibling())
        return result;
    }
  for (; ; ) {
    if (after != null && cur.type.is(after))
      return result;
    if (cur.type.is(type))
      result.push(cur.node);
    if (!cur.nextSibling())
      return after == null ? result : [];
  }
}
function matchNodeContext(node, context, i = context.length - 1) {
  for (let p = node; i >= 0; p = p.parent) {
    if (!p)
      return false;
    if (!p.type.isAnonymous) {
      if (context[i] && context[i] != p.name)
        return false;
      i--;
    }
  }
  return true;
}
var BufferContext = class {
  constructor(parent, buffer, index, start) {
    this.parent = parent;
    this.buffer = buffer;
    this.index = index;
    this.start = start;
  }
};
var BufferNode = class _BufferNode extends BaseNode {
  get name() {
    return this.type.name;
  }
  get from() {
    return this.context.start + this.context.buffer.buffer[this.index + 1];
  }
  get to() {
    return this.context.start + this.context.buffer.buffer[this.index + 2];
  }
  constructor(context, _parent, index) {
    super();
    this.context = context;
    this._parent = _parent;
    this.index = index;
    this.type = context.buffer.set.types[context.buffer.buffer[index]];
  }
  child(dir, pos, side) {
    let { buffer } = this.context;
    let index = buffer.findChild(this.index + 4, buffer.buffer[this.index + 3], dir, pos - this.context.start, side);
    return index < 0 ? null : new _BufferNode(this.context, this, index);
  }
  get firstChild() {
    return this.child(
      1,
      0,
      4
      /* Side.DontCare */
    );
  }
  get lastChild() {
    return this.child(
      -1,
      0,
      4
      /* Side.DontCare */
    );
  }
  childAfter(pos) {
    return this.child(
      1,
      pos,
      2
      /* Side.After */
    );
  }
  childBefore(pos) {
    return this.child(
      -1,
      pos,
      -2
      /* Side.Before */
    );
  }
  prop(prop) {
    return this.type.prop(prop);
  }
  enter(pos, side, mode = 0) {
    if (mode & IterMode.ExcludeBuffers)
      return null;
    let { buffer } = this.context;
    let index = buffer.findChild(this.index + 4, buffer.buffer[this.index + 3], side > 0 ? 1 : -1, pos - this.context.start, side);
    return index < 0 ? null : new _BufferNode(this.context, this, index);
  }
  get parent() {
    return this._parent || this.context.parent.nextSignificantParent();
  }
  externalSibling(dir) {
    return this._parent ? null : this.context.parent.nextChild(
      this.context.index + dir,
      dir,
      0,
      4
      /* Side.DontCare */
    );
  }
  get nextSibling() {
    let { buffer } = this.context;
    let after = buffer.buffer[this.index + 3];
    if (after < (this._parent ? buffer.buffer[this._parent.index + 3] : buffer.buffer.length))
      return new _BufferNode(this.context, this._parent, after);
    return this.externalSibling(1);
  }
  get prevSibling() {
    let { buffer } = this.context;
    let parentStart = this._parent ? this._parent.index + 4 : 0;
    if (this.index == parentStart)
      return this.externalSibling(-1);
    return new _BufferNode(this.context, this._parent, buffer.findChild(
      parentStart,
      this.index,
      -1,
      0,
      4
      /* Side.DontCare */
    ));
  }
  get tree() {
    return null;
  }
  toTree() {
    let children = [], positions = [];
    let { buffer } = this.context;
    let startI = this.index + 4, endI = buffer.buffer[this.index + 3];
    if (endI > startI) {
      let from = buffer.buffer[this.index + 1];
      children.push(buffer.slice(startI, endI, from));
      positions.push(0);
    }
    return new Tree(this.type, children, positions, this.to - this.from);
  }
  /**
  @internal
  */
  toString() {
    return this.context.buffer.childString(this.index);
  }
};
function iterStack(heads) {
  if (!heads.length)
    return null;
  let pick = 0, picked = heads[0];
  for (let i = 1; i < heads.length; i++) {
    let node = heads[i];
    if (node.from > picked.from || node.to < picked.to) {
      picked = node;
      pick = i;
    }
  }
  let next = picked instanceof TreeNode && picked.index < 0 ? null : picked.parent;
  let newHeads = heads.slice();
  if (next)
    newHeads[pick] = next;
  else
    newHeads.splice(pick, 1);
  return new StackIterator(newHeads, picked);
}
var StackIterator = class {
  constructor(heads, node) {
    this.heads = heads;
    this.node = node;
  }
  get next() {
    return iterStack(this.heads);
  }
};
function stackIterator(tree, pos, side) {
  let inner = tree.resolveInner(pos, side), layers = null;
  for (let scan = inner instanceof TreeNode ? inner : inner.context.parent; scan; scan = scan.parent) {
    if (scan.index < 0) {
      let parent = scan.parent;
      (layers || (layers = [inner])).push(parent.resolve(pos, side));
      scan = parent;
    } else {
      let mount = MountedTree.get(scan.tree);
      if (mount && mount.overlay && mount.overlay[0].from <= pos && mount.overlay[mount.overlay.length - 1].to >= pos) {
        let root = new TreeNode(mount.tree, mount.overlay[0].from + scan.from, -1, scan);
        (layers || (layers = [inner])).push(resolveNode(root, pos, side, false));
      }
    }
  }
  return layers ? iterStack(layers) : inner;
}
var TreeCursor = class {
  /**
  Shorthand for `.type.name`.
  */
  get name() {
    return this.type.name;
  }
  /**
  @internal
  */
  constructor(node, mode = 0) {
    this.buffer = null;
    this.stack = [];
    this.index = 0;
    this.bufferNode = null;
    this.mode = mode & ~IterMode.EnterBracketed;
    if (node instanceof TreeNode) {
      this.yieldNode(node);
    } else {
      this._tree = node.context.parent;
      this.buffer = node.context;
      for (let n = node._parent; n; n = n._parent)
        this.stack.unshift(n.index);
      this.bufferNode = node;
      this.yieldBuf(node.index);
    }
  }
  yieldNode(node) {
    if (!node)
      return false;
    this._tree = node;
    this.type = node.type;
    this.from = node.from;
    this.to = node.to;
    return true;
  }
  yieldBuf(index, type) {
    this.index = index;
    let { start, buffer } = this.buffer;
    this.type = type || buffer.set.types[buffer.buffer[index]];
    this.from = start + buffer.buffer[index + 1];
    this.to = start + buffer.buffer[index + 2];
    return true;
  }
  /**
  @internal
  */
  yield(node) {
    if (!node)
      return false;
    if (node instanceof TreeNode) {
      this.buffer = null;
      return this.yieldNode(node);
    }
    this.buffer = node.context;
    return this.yieldBuf(node.index, node.type);
  }
  /**
  @internal
  */
  toString() {
    return this.buffer ? this.buffer.buffer.childString(this.index) : this._tree.toString();
  }
  /**
  @internal
  */
  enterChild(dir, pos, side) {
    if (!this.buffer)
      return this.yield(this._tree.nextChild(dir < 0 ? this._tree._tree.children.length - 1 : 0, dir, pos, side, this.mode));
    let { buffer } = this.buffer;
    let index = buffer.findChild(this.index + 4, buffer.buffer[this.index + 3], dir, pos - this.buffer.start, side);
    if (index < 0)
      return false;
    this.stack.push(this.index);
    return this.yieldBuf(index);
  }
  /**
  Move the cursor to this node's first child. When this returns
  false, the node has no child, and the cursor has not been moved.
  */
  firstChild() {
    return this.enterChild(
      1,
      0,
      4
      /* Side.DontCare */
    );
  }
  /**
  Move the cursor to this node's last child.
  */
  lastChild() {
    return this.enterChild(
      -1,
      0,
      4
      /* Side.DontCare */
    );
  }
  /**
  Move the cursor to the first child that ends after `pos`.
  */
  childAfter(pos) {
    return this.enterChild(
      1,
      pos,
      2
      /* Side.After */
    );
  }
  /**
  Move to the last child that starts before `pos`.
  */
  childBefore(pos) {
    return this.enterChild(
      -1,
      pos,
      -2
      /* Side.Before */
    );
  }
  /**
  Move the cursor to the child around `pos`. If side is -1 the
  child may end at that position, when 1 it may start there. This
  will also enter [overlaid](#common.MountedTree.overlay)
  [mounted](#common.NodeProp^mounted) trees unless `overlays` is
  set to false.
  */
  enter(pos, side, mode = this.mode) {
    if (!this.buffer)
      return this.yield(this._tree.enter(pos, side, mode));
    return mode & IterMode.ExcludeBuffers ? false : this.enterChild(1, pos, side);
  }
  /**
  Move to the node's parent node, if this isn't the top node.
  */
  parent() {
    if (!this.buffer)
      return this.yieldNode(this.mode & IterMode.IncludeAnonymous ? this._tree._parent : this._tree.parent);
    if (this.stack.length)
      return this.yieldBuf(this.stack.pop());
    let parent = this.mode & IterMode.IncludeAnonymous ? this.buffer.parent : this.buffer.parent.nextSignificantParent();
    this.buffer = null;
    return this.yieldNode(parent);
  }
  /**
  @internal
  */
  sibling(dir) {
    if (!this.buffer)
      return !this._tree._parent ? false : this.yield(this._tree.index < 0 ? null : this._tree._parent.nextChild(this._tree.index + dir, dir, 0, 4, this.mode));
    let { buffer } = this.buffer, d = this.stack.length - 1;
    if (dir < 0) {
      let parentStart = d < 0 ? 0 : this.stack[d] + 4;
      if (this.index != parentStart)
        return this.yieldBuf(buffer.findChild(
          parentStart,
          this.index,
          -1,
          0,
          4
          /* Side.DontCare */
        ));
    } else {
      let after = buffer.buffer[this.index + 3];
      if (after < (d < 0 ? buffer.buffer.length : buffer.buffer[this.stack[d] + 3]))
        return this.yieldBuf(after);
    }
    return d < 0 ? this.yield(this.buffer.parent.nextChild(this.buffer.index + dir, dir, 0, 4, this.mode)) : false;
  }
  /**
  Move to this node's next sibling, if any.
  */
  nextSibling() {
    return this.sibling(1);
  }
  /**
  Move to this node's previous sibling, if any.
  */
  prevSibling() {
    return this.sibling(-1);
  }
  atLastNode(dir) {
    let index, parent, { buffer } = this;
    if (buffer) {
      if (dir > 0) {
        if (this.index < buffer.buffer.buffer.length)
          return false;
      } else {
        for (let i = 0; i < this.index; i++)
          if (buffer.buffer.buffer[i + 3] < this.index)
            return false;
      }
      ({ index, parent } = buffer);
    } else {
      ({ index, _parent: parent } = this._tree);
    }
    for (; parent; { index, _parent: parent } = parent) {
      if (index > -1)
        for (let i = index + dir, e = dir < 0 ? -1 : parent._tree.children.length; i != e; i += dir) {
          let child = parent._tree.children[i];
          if (this.mode & IterMode.IncludeAnonymous || child instanceof TreeBuffer || !child.type.isAnonymous || hasChild(child))
            return false;
        }
    }
    return true;
  }
  move(dir, enter) {
    if (enter && this.enterChild(
      dir,
      0,
      4
      /* Side.DontCare */
    ))
      return true;
    for (; ; ) {
      if (this.sibling(dir))
        return true;
      if (this.atLastNode(dir) || !this.parent())
        return false;
    }
  }
  /**
  Move to the next node in a
  [pre-order](https://en.wikipedia.org/wiki/Tree_traversal#Pre-order,_NLR)
  traversal, going from a node to its first child or, if the
  current node is empty or `enter` is false, its next sibling or
  the next sibling of the first parent node that has one.
  */
  next(enter = true) {
    return this.move(1, enter);
  }
  /**
  Move to the next node in a last-to-first pre-order traversal. A
  node is followed by its last child or, if it has none, its
  previous sibling or the previous sibling of the first parent
  node that has one.
  */
  prev(enter = true) {
    return this.move(-1, enter);
  }
  /**
  Move the cursor to the innermost node that covers `pos`. If
  `side` is -1, it will enter nodes that end at `pos`. If it is 1,
  it will enter nodes that start at `pos`.
  */
  moveTo(pos, side = 0) {
    while (this.from == this.to || (side < 1 ? this.from >= pos : this.from > pos) || (side > -1 ? this.to <= pos : this.to < pos))
      if (!this.parent())
        break;
    while (this.enterChild(1, pos, side)) {
    }
    return this;
  }
  /**
  Get a [syntax node](#common.SyntaxNode) at the cursor's current
  position.
  */
  get node() {
    if (!this.buffer)
      return this._tree;
    let cache = this.bufferNode, result = null, depth = 0;
    if (cache && cache.context == this.buffer) {
      scan: for (let index = this.index, d = this.stack.length; d >= 0; ) {
        for (let c = cache; c; c = c._parent)
          if (c.index == index) {
            if (index == this.index)
              return c;
            result = c;
            depth = d + 1;
            break scan;
          }
        index = this.stack[--d];
      }
    }
    for (let i = depth; i < this.stack.length; i++)
      result = new BufferNode(this.buffer, result, this.stack[i]);
    return this.bufferNode = new BufferNode(this.buffer, result, this.index);
  }
  /**
  Get the [tree](#common.Tree) that represents the current node, if
  any. Will return null when the node is in a [tree
  buffer](#common.TreeBuffer).
  */
  get tree() {
    return this.buffer ? null : this._tree._tree;
  }
  /**
  Iterate over the current node and all its descendants, calling
  `enter` when entering a node and `leave`, if given, when leaving
  one. When `enter` returns `false`, any children of that node are
  skipped, and `leave` isn't called for it.
  */
  iterate(enter, leave) {
    for (let depth = 0; ; ) {
      let mustLeave = false;
      if (this.type.isAnonymous || enter(this) !== false) {
        if (this.firstChild()) {
          depth++;
          continue;
        }
        if (!this.type.isAnonymous)
          mustLeave = true;
      }
      for (; ; ) {
        if (mustLeave && leave)
          leave(this);
        mustLeave = this.type.isAnonymous;
        if (!depth)
          return;
        if (this.nextSibling())
          break;
        this.parent();
        depth--;
        mustLeave = true;
      }
    }
  }
  /**
  Test whether the current node matches a given context—a sequence
  of direct parent node names. Empty strings in the context array
  are treated as wildcards.
  */
  matchContext(context) {
    if (!this.buffer)
      return matchNodeContext(this.node.parent, context);
    let { buffer } = this.buffer, { types } = buffer.set;
    for (let i = context.length - 1, d = this.stack.length - 1; i >= 0; d--) {
      if (d < 0)
        return matchNodeContext(this._tree, context, i);
      let type = types[buffer.buffer[this.stack[d]]];
      if (!type.isAnonymous) {
        if (context[i] && context[i] != type.name)
          return false;
        i--;
      }
    }
    return true;
  }
};
function hasChild(tree) {
  return tree.children.some((ch) => ch instanceof TreeBuffer || !ch.type.isAnonymous || hasChild(ch));
}
function buildTree(data) {
  var _a;
  let { buffer, nodeSet, maxBufferLength = DefaultBufferLength, reused = [], minRepeatType = nodeSet.types.length } = data;
  let cursor = Array.isArray(buffer) ? new FlatBufferCursor(buffer, buffer.length) : buffer;
  let types = nodeSet.types;
  let contextHash = 0, lookAhead = 0;
  function takeNode(parentStart, minPos, children2, positions2, inRepeat, depth) {
    let { id: id2, start, end, size } = cursor;
    let lookAheadAtStart = lookAhead, contextAtStart = contextHash;
    if (size < 0) {
      cursor.next();
      if (size == -1) {
        let node2 = reused[id2];
        children2.push(node2);
        positions2.push(start - parentStart);
        return;
      } else if (size == -3) {
        contextHash = id2;
        return;
      } else if (size == -4) {
        lookAhead = id2;
        return;
      } else {
        throw new RangeError(`Unrecognized record size: ${size}`);
      }
    }
    let type = types[id2], node, buffer2;
    let startPos = start - parentStart;
    if (end - start <= maxBufferLength && (buffer2 = findBufferSize(cursor.pos - minPos, inRepeat))) {
      let data2 = new Uint16Array(buffer2.size - buffer2.skip);
      let endPos = cursor.pos - buffer2.size, index = data2.length;
      while (cursor.pos > endPos)
        index = copyToBuffer(buffer2.start, data2, index);
      node = new TreeBuffer(data2, end - buffer2.start, nodeSet);
      startPos = buffer2.start - parentStart;
    } else {
      let endPos = cursor.pos - size;
      cursor.next();
      let localChildren = [], localPositions = [];
      let localInRepeat = id2 >= minRepeatType ? id2 : -1;
      let lastGroup = 0, lastEnd = end;
      while (cursor.pos > endPos) {
        if (localInRepeat >= 0 && cursor.id == localInRepeat && cursor.size >= 0) {
          if (cursor.end <= lastEnd - maxBufferLength) {
            makeRepeatLeaf(localChildren, localPositions, start, lastGroup, cursor.end, lastEnd, localInRepeat, lookAheadAtStart, contextAtStart);
            lastGroup = localChildren.length;
            lastEnd = cursor.end;
          }
          cursor.next();
        } else if (depth > 2500) {
          takeFlatNode(start, endPos, localChildren, localPositions);
        } else {
          takeNode(start, endPos, localChildren, localPositions, localInRepeat, depth + 1);
        }
      }
      if (localInRepeat >= 0 && lastGroup > 0 && lastGroup < localChildren.length)
        makeRepeatLeaf(localChildren, localPositions, start, lastGroup, start, lastEnd, localInRepeat, lookAheadAtStart, contextAtStart);
      localChildren.reverse();
      localPositions.reverse();
      if (localInRepeat > -1 && lastGroup > 0) {
        let make = makeBalanced(type, contextAtStart);
        node = balanceRange(type, localChildren, localPositions, 0, localChildren.length, 0, end - start, make, make);
      } else {
        node = makeTree(type, localChildren, localPositions, end - start, lookAheadAtStart - end, contextAtStart);
      }
    }
    children2.push(node);
    positions2.push(startPos);
  }
  function takeFlatNode(parentStart, minPos, children2, positions2) {
    let nodes = [];
    let nodeCount = 0, stopAt = -1;
    while (cursor.pos > minPos) {
      let { id: id2, start, end, size } = cursor;
      if (size > 4) {
        cursor.next();
      } else if (stopAt > -1 && start < stopAt) {
        break;
      } else {
        if (stopAt < 0)
          stopAt = end - maxBufferLength;
        nodes.push(id2, start, end);
        nodeCount++;
        cursor.next();
      }
    }
    if (nodeCount) {
      let buffer2 = new Uint16Array(nodeCount * 4);
      let start = nodes[nodes.length - 2];
      for (let i = nodes.length - 3, j = 0; i >= 0; i -= 3) {
        buffer2[j++] = nodes[i];
        buffer2[j++] = nodes[i + 1] - start;
        buffer2[j++] = nodes[i + 2] - start;
        buffer2[j++] = j;
      }
      children2.push(new TreeBuffer(buffer2, nodes[2] - start, nodeSet));
      positions2.push(start - parentStart);
    }
  }
  function makeBalanced(type, contextHash2) {
    return (children2, positions2, length2) => {
      let lookAhead2 = 0, lastI = children2.length - 1, last, lookAheadProp;
      if (lastI >= 0 && (last = children2[lastI]) instanceof Tree) {
        if (!lastI && last.type == type && last.length == length2)
          return last;
        if (lookAheadProp = last.prop(NodeProp.lookAhead))
          lookAhead2 = positions2[lastI] + last.length + lookAheadProp;
      }
      return makeTree(type, children2, positions2, length2, lookAhead2, contextHash2);
    };
  }
  function makeRepeatLeaf(children2, positions2, base, i, from, to, type, lookAhead2, contextHash2) {
    let localChildren = [], localPositions = [];
    while (children2.length > i) {
      localChildren.push(children2.pop());
      localPositions.push(positions2.pop() + base - from);
    }
    children2.push(makeTree(nodeSet.types[type], localChildren, localPositions, to - from, lookAhead2 - to, contextHash2));
    positions2.push(from - base);
  }
  function makeTree(type, children2, positions2, length2, lookAhead2, contextHash2, props) {
    if (contextHash2) {
      let pair2 = [NodeProp.contextHash, contextHash2];
      props = props ? [pair2].concat(props) : [pair2];
    }
    if (lookAhead2 > 25) {
      let pair2 = [NodeProp.lookAhead, lookAhead2];
      props = props ? [pair2].concat(props) : [pair2];
    }
    return new Tree(type, children2, positions2, length2, props);
  }
  function findBufferSize(maxSize, inRepeat) {
    let fork = cursor.fork();
    let size = 0, start = 0, skip = 0, minStart = fork.end - maxBufferLength;
    let result = { size: 0, start: 0, skip: 0 };
    scan: for (let minPos = fork.pos - maxSize; fork.pos > minPos; ) {
      let nodeSize2 = fork.size;
      if (fork.id == inRepeat && nodeSize2 >= 0) {
        result.size = size;
        result.start = start;
        result.skip = skip;
        skip += 4;
        size += 4;
        fork.next();
        continue;
      }
      let startPos = fork.pos - nodeSize2;
      if (nodeSize2 < 0 || startPos < minPos || fork.start < minStart)
        break;
      let localSkipped = fork.id >= minRepeatType ? 4 : 0;
      let nodeStart = fork.start;
      fork.next();
      while (fork.pos > startPos) {
        if (fork.size < 0) {
          if (fork.size == -3 || fork.size == -4)
            localSkipped += 4;
          else
            break scan;
        } else if (fork.id >= minRepeatType) {
          localSkipped += 4;
        }
        fork.next();
      }
      start = nodeStart;
      size += nodeSize2;
      skip += localSkipped;
    }
    if (inRepeat < 0 || size == maxSize) {
      result.size = size;
      result.start = start;
      result.skip = skip;
    }
    return result.size > 4 ? result : void 0;
  }
  function copyToBuffer(bufferStart, buffer2, index) {
    let { id: id2, start, end, size } = cursor;
    cursor.next();
    if (size >= 0 && id2 < minRepeatType) {
      let startIndex = index;
      if (size > 4) {
        let endPos = cursor.pos - (size - 4);
        while (cursor.pos > endPos)
          index = copyToBuffer(bufferStart, buffer2, index);
      }
      buffer2[--index] = startIndex;
      buffer2[--index] = end - bufferStart;
      buffer2[--index] = start - bufferStart;
      buffer2[--index] = id2;
    } else if (size == -3) {
      contextHash = id2;
    } else if (size == -4) {
      lookAhead = id2;
    }
    return index;
  }
  let children = [], positions = [];
  while (cursor.pos > 0)
    takeNode(data.start || 0, data.bufferStart || 0, children, positions, -1, 0);
  let length = (_a = data.length) !== null && _a !== void 0 ? _a : children.length ? positions[0] + children[0].length : 0;
  return new Tree(types[data.topID], children.reverse(), positions.reverse(), length);
}
var nodeSizeCache = /* @__PURE__ */ new WeakMap();
function nodeSize(balanceType, node) {
  if (!balanceType.isAnonymous || node instanceof TreeBuffer || node.type != balanceType)
    return 1;
  let size = nodeSizeCache.get(node);
  if (size == null) {
    size = 1;
    for (let child of node.children) {
      if (child.type != balanceType || !(child instanceof Tree)) {
        size = 1;
        break;
      }
      size += nodeSize(balanceType, child);
    }
    nodeSizeCache.set(node, size);
  }
  return size;
}
function balanceRange(balanceType, children, positions, from, to, start, length, mkTop, mkTree) {
  let total = 0;
  for (let i = from; i < to; i++)
    total += nodeSize(balanceType, children[i]);
  let maxChild = Math.ceil(
    total * 1.5 / 8
    /* Balance.BranchFactor */
  );
  let localChildren = [], localPositions = [];
  function divide(children2, positions2, from2, to2, offset) {
    for (let i = from2; i < to2; ) {
      let groupFrom = i, groupStart = positions2[i], groupSize = nodeSize(balanceType, children2[i]);
      i++;
      for (; i < to2; i++) {
        let nextSize = nodeSize(balanceType, children2[i]);
        if (groupSize + nextSize >= maxChild)
          break;
        groupSize += nextSize;
      }
      if (i == groupFrom + 1) {
        if (groupSize > maxChild) {
          let only = children2[groupFrom];
          divide(only.children, only.positions, 0, only.children.length, positions2[groupFrom] + offset);
          continue;
        }
        localChildren.push(children2[groupFrom]);
      } else {
        let length2 = positions2[i - 1] + children2[i - 1].length - groupStart;
        localChildren.push(balanceRange(balanceType, children2, positions2, groupFrom, i, groupStart, length2, null, mkTree));
      }
      localPositions.push(groupStart + offset - start);
    }
  }
  divide(children, positions, from, to, 0);
  return (mkTop || mkTree)(localChildren, localPositions, length);
}
var Parser = class {
  /**
  Start a parse, returning a [partial parse](#common.PartialParse)
  object. [`fragments`](#common.TreeFragment) can be passed in to
  make the parse incremental.
  
  By default, the entire input is parsed. You can pass `ranges`,
  which should be a sorted array of non-empty, non-overlapping
  ranges, to parse only those ranges. The tree returned in that
  case will start at `ranges[0].from`.
  */
  startParse(input, fragments, ranges) {
    if (typeof input == "string")
      input = new StringInput(input);
    ranges = !ranges ? [new Range(0, input.length)] : ranges.length ? ranges.map((r) => new Range(r.from, r.to)) : [new Range(0, 0)];
    return this.createParse(input, fragments || [], ranges);
  }
  /**
  Run a full parse, returning the resulting tree.
  */
  parse(input, fragments, ranges) {
    let parse = this.startParse(input, fragments, ranges);
    for (; ; ) {
      let done = parse.advance();
      if (done)
        return done;
    }
  }
};
var StringInput = class {
  constructor(string2) {
    this.string = string2;
  }
  get length() {
    return this.string.length;
  }
  chunk(from) {
    return this.string.slice(from);
  }
  get lineChunks() {
    return false;
  }
  read(from, to) {
    return this.string.slice(from, to);
  }
};
var stoppedInner = new NodeProp({ perNode: true });

// node_modules/@lezer/lr/dist/index.js
var Stack = class _Stack {
  /**
  @internal
  */
  constructor(p, stack, state, reducePos, pos, score, buffer, bufferBase, curContext, lookAhead = 0, parent) {
    this.p = p;
    this.stack = stack;
    this.state = state;
    this.reducePos = reducePos;
    this.pos = pos;
    this.score = score;
    this.buffer = buffer;
    this.bufferBase = bufferBase;
    this.curContext = curContext;
    this.lookAhead = lookAhead;
    this.parent = parent;
  }
  /**
  @internal
  */
  toString() {
    return `[${this.stack.filter((_, i) => i % 3 == 0).concat(this.state)}]@${this.pos}${this.score ? "!" + this.score : ""}`;
  }
  // Start an empty stack
  /**
  @internal
  */
  static start(p, state, pos = 0) {
    let cx = p.parser.context;
    return new _Stack(p, [], state, pos, pos, 0, [], 0, cx ? new StackContext(cx, cx.start) : null, 0, null);
  }
  /**
  The stack's current [context](#lr.ContextTracker) value, if
  any. Its type will depend on the context tracker's type
  parameter, or it will be `null` if there is no context
  tracker.
  */
  get context() {
    return this.curContext ? this.curContext.context : null;
  }
  // Push a state onto the stack, tracking its start position as well
  // as the buffer base at that point.
  /**
  @internal
  */
  pushState(state, start) {
    this.stack.push(this.state, start, this.bufferBase + this.buffer.length);
    this.state = state;
  }
  // Apply a reduce action
  /**
  @internal
  */
  reduce(action) {
    var _a;
    let depth = action >> 19, type = action & 65535;
    let { parser: parser2 } = this.p;
    let lookaheadRecord = this.reducePos < this.pos - 25 && this.setLookAhead(this.pos);
    let dPrec = parser2.dynamicPrecedence(type);
    if (dPrec)
      this.score += dPrec;
    if (depth == 0) {
      if (type < parser2.minRepeatTerm && this.reducePos < this.pos)
        this.reducePos = this.pos;
      this.pushState(parser2.getGoto(this.state, type, true), this.reducePos);
      if (type < parser2.minRepeatTerm)
        this.storeNode(type, this.reducePos, this.reducePos, lookaheadRecord ? 8 : 4, true);
      this.reduceContext(type, this.reducePos);
      return;
    }
    let base = this.stack.length - (depth - 1) * 3 - (action & 262144 ? 6 : 0);
    let start = base ? this.stack[base - 2] : this.p.ranges[0].from;
    if (type < parser2.minRepeatTerm && start == this.reducePos && this.reducePos < this.pos)
      this.reducePos = this.pos;
    let size = this.reducePos - start;
    if (size >= 2e3 && !((_a = this.p.parser.nodeSet.types[type]) === null || _a === void 0 ? void 0 : _a.isAnonymous)) {
      if (start == this.p.lastBigReductionStart) {
        this.p.bigReductionCount++;
        this.p.lastBigReductionSize = size;
      } else if (this.p.lastBigReductionSize < size) {
        this.p.bigReductionCount = 1;
        this.p.lastBigReductionStart = start;
        this.p.lastBigReductionSize = size;
      }
    }
    let bufferBase = base ? this.stack[base - 1] : 0, count = this.bufferBase + this.buffer.length - bufferBase;
    if (type < parser2.minRepeatTerm || action & 131072) {
      let pos = parser2.stateFlag(
        this.state,
        1
        /* StateFlag.Skipped */
      ) ? this.pos : this.reducePos;
      this.storeNode(type, start, pos, count + 4, true);
    }
    if (action & 262144) {
      this.state = this.stack[base];
    } else {
      let baseStateID = this.stack[base - 3];
      this.state = parser2.getGoto(baseStateID, type, true);
    }
    while (this.stack.length > base)
      this.stack.pop();
    this.reduceContext(type, start);
  }
  // Shift a value into the buffer
  /**
  @internal
  */
  storeNode(term, start, end, size = 4, mustSink = false) {
    if (term == 0 && (!this.stack.length || this.stack[this.stack.length - 1] < this.buffer.length + this.bufferBase)) {
      let top = this.buffer.length;
      if (top > 0 && this.buffer[top - 4] == 0 && this.buffer[top - 1] > -1) {
        if (start == end)
          return;
        if (this.buffer[top - 2] >= start) {
          this.buffer[top - 2] = end;
          return;
        }
      }
    }
    if (!mustSink || this.pos == end) {
      this.buffer.push(term, start, end, size);
    } else {
      let index = this.buffer.length;
      if (index > 0 && (this.buffer[index - 4] != 0 || this.buffer[index - 1] < 0)) {
        let mustMove = false;
        for (let scan = index; scan > 0 && this.buffer[scan - 2] > end; scan -= 4) {
          if (this.buffer[scan - 1] >= 0) {
            mustMove = true;
            break;
          }
        }
        if (mustMove)
          while (index > 0 && this.buffer[index - 2] > end) {
            this.buffer[index] = this.buffer[index - 4];
            this.buffer[index + 1] = this.buffer[index - 3];
            this.buffer[index + 2] = this.buffer[index - 2];
            this.buffer[index + 3] = this.buffer[index - 1];
            index -= 4;
            if (size > 4)
              size -= 4;
          }
      }
      this.buffer[index] = term;
      this.buffer[index + 1] = start;
      this.buffer[index + 2] = end;
      this.buffer[index + 3] = size;
    }
  }
  // Apply a shift action
  /**
  @internal
  */
  shift(action, type, start, end) {
    if (action & 131072) {
      this.pushState(action & 65535, this.pos);
    } else if ((action & 262144) == 0) {
      let nextState = action, { parser: parser2 } = this.p;
      this.pos = end;
      let skipped = parser2.stateFlag(
        nextState,
        1
        /* StateFlag.Skipped */
      );
      if (!skipped && (end > start || type <= parser2.maxNode))
        this.reducePos = end;
      this.pushState(nextState, skipped ? start : Math.min(start, this.reducePos));
      this.shiftContext(type, start);
      if (type <= parser2.maxNode)
        this.buffer.push(type, start, end, 4);
    } else {
      this.pos = end;
      this.shiftContext(type, start);
      if (type <= this.p.parser.maxNode)
        this.buffer.push(type, start, end, 4);
    }
  }
  // Apply an action
  /**
  @internal
  */
  apply(action, next, nextStart, nextEnd) {
    if (action & 65536)
      this.reduce(action);
    else
      this.shift(action, next, nextStart, nextEnd);
  }
  // Add a prebuilt (reused) node into the buffer.
  /**
  @internal
  */
  useNode(value, next) {
    let index = this.p.reused.length - 1;
    if (index < 0 || this.p.reused[index] != value) {
      this.p.reused.push(value);
      index++;
    }
    let start = this.pos;
    this.reducePos = this.pos = start + value.length;
    this.pushState(next, start);
    this.buffer.push(
      index,
      start,
      this.reducePos,
      -1
      /* size == -1 means this is a reused value */
    );
    if (this.curContext)
      this.updateContext(this.curContext.tracker.reuse(this.curContext.context, value, this, this.p.stream.reset(this.pos - value.length)));
  }
  // Split the stack. Due to the buffer sharing and the fact
  // that `this.stack` tends to stay quite shallow, this isn't very
  // expensive.
  /**
  @internal
  */
  split() {
    let parent = this;
    let off = parent.buffer.length;
    if (off && parent.buffer[off - 4] == 0)
      off -= 4;
    while (off > 0 && parent.buffer[off - 2] > parent.reducePos)
      off -= 4;
    let buffer = parent.buffer.slice(off), base = parent.bufferBase + off;
    while (parent && base == parent.bufferBase)
      parent = parent.parent;
    return new _Stack(this.p, this.stack.slice(), this.state, this.reducePos, this.pos, this.score, buffer, base, this.curContext, this.lookAhead, parent);
  }
  // Try to recover from an error by 'deleting' (ignoring) one token.
  /**
  @internal
  */
  recoverByDelete(next, nextEnd) {
    let isNode = next <= this.p.parser.maxNode;
    if (isNode)
      this.storeNode(next, this.pos, nextEnd, 4);
    this.storeNode(0, this.pos, nextEnd, isNode ? 8 : 4);
    this.pos = this.reducePos = nextEnd;
    this.score -= 190;
  }
  /**
  Check if the given term would be able to be shifted (optionally
  after some reductions) on this stack. This can be useful for
  external tokenizers that want to make sure they only provide a
  given token when it applies.
  */
  canShift(term) {
    for (let sim = new SimulatedStack(this); ; ) {
      let action = this.p.parser.stateSlot(
        sim.state,
        4
        /* ParseState.DefaultReduce */
      ) || this.p.parser.hasAction(sim.state, term);
      if (action == 0)
        return false;
      if ((action & 65536) == 0)
        return true;
      sim.reduce(action);
    }
  }
  // Apply up to Recover.MaxNext recovery actions that conceptually
  // inserts some missing token or rule.
  /**
  @internal
  */
  recoverByInsert(next) {
    if (this.stack.length >= 300)
      return [];
    let nextStates = this.p.parser.nextStates(this.state);
    if (nextStates.length > 4 << 1 || this.stack.length >= 120) {
      let best = [];
      for (let i = 0, s; i < nextStates.length; i += 2) {
        if ((s = nextStates[i + 1]) != this.state && this.p.parser.hasAction(s, next))
          best.push(nextStates[i], s);
      }
      if (this.stack.length < 120)
        for (let i = 0; best.length < 4 << 1 && i < nextStates.length; i += 2) {
          let s = nextStates[i + 1];
          if (!best.some((v, i2) => i2 & 1 && v == s))
            best.push(nextStates[i], s);
        }
      nextStates = best;
    }
    let result = [];
    for (let i = 0; i < nextStates.length && result.length < 4; i += 2) {
      let s = nextStates[i + 1];
      if (s == this.state)
        continue;
      let stack = this.split();
      stack.pushState(s, this.pos);
      stack.storeNode(0, stack.pos, stack.pos, 4, true);
      stack.shiftContext(nextStates[i], this.pos);
      stack.reducePos = this.pos;
      stack.score -= 200;
      result.push(stack);
    }
    return result;
  }
  // Force a reduce, if possible. Return false if that can't
  // be done.
  /**
  @internal
  */
  forceReduce() {
    let { parser: parser2 } = this.p;
    let reduce = parser2.stateSlot(
      this.state,
      5
      /* ParseState.ForcedReduce */
    );
    if ((reduce & 65536) == 0)
      return false;
    if (!parser2.validAction(this.state, reduce)) {
      let depth = reduce >> 19, term = reduce & 65535;
      let target = this.stack.length - depth * 3;
      if (target < 0 || parser2.getGoto(this.stack[target], term, false) < 0) {
        let backup = this.findForcedReduction();
        if (backup == null)
          return false;
        reduce = backup;
      }
      this.storeNode(0, this.pos, this.pos, 4, true);
      this.score -= 100;
    }
    this.reducePos = this.pos;
    this.reduce(reduce);
    return true;
  }
  /**
  Try to scan through the automaton to find some kind of reduction
  that can be applied. Used when the regular ForcedReduce field
  isn't a valid action. @internal
  */
  findForcedReduction() {
    let { parser: parser2 } = this.p, seen = [];
    let explore = (state, depth) => {
      if (seen.includes(state))
        return;
      seen.push(state);
      return parser2.allActions(state, (action) => {
        if (action & (262144 | 131072)) ;
        else if (action & 65536) {
          let rDepth = (action >> 19) - depth;
          if (rDepth > 1) {
            let term = action & 65535, target = this.stack.length - rDepth * 3;
            if (target >= 0 && parser2.getGoto(this.stack[target], term, false) >= 0)
              return rDepth << 19 | 65536 | term;
          }
        } else {
          let found = explore(action, depth + 1);
          if (found != null)
            return found;
        }
      });
    };
    return explore(this.state, 0);
  }
  /**
  @internal
  */
  forceAll() {
    while (!this.p.parser.stateFlag(
      this.state,
      2
      /* StateFlag.Accepting */
    )) {
      if (!this.forceReduce()) {
        this.storeNode(0, this.pos, this.pos, 4, true);
        break;
      }
    }
    return this;
  }
  /**
  Check whether this state has no further actions (assumed to be a direct descendant of the
  top state, since any other states must be able to continue
  somehow). @internal
  */
  get deadEnd() {
    if (this.stack.length != 3)
      return false;
    let { parser: parser2 } = this.p;
    return parser2.data[parser2.stateSlot(
      this.state,
      1
      /* ParseState.Actions */
    )] == 65535 && !parser2.stateSlot(
      this.state,
      4
      /* ParseState.DefaultReduce */
    );
  }
  /**
  Restart the stack (put it back in its start state). Only safe
  when this.stack.length == 3 (state is directly below the top
  state). @internal
  */
  restart() {
    this.storeNode(0, this.pos, this.pos, 4, true);
    this.state = this.stack[0];
    this.stack.length = 0;
  }
  /**
  @internal
  */
  sameState(other) {
    if (this.state != other.state || this.stack.length != other.stack.length)
      return false;
    for (let i = 0; i < this.stack.length; i += 3)
      if (this.stack[i] != other.stack[i])
        return false;
    return true;
  }
  /**
  Get the parser used by this stack.
  */
  get parser() {
    return this.p.parser;
  }
  /**
  Test whether a given dialect (by numeric ID, as exported from
  the terms file) is enabled.
  */
  dialectEnabled(dialectID) {
    return this.p.parser.dialect.flags[dialectID];
  }
  shiftContext(term, start) {
    if (this.curContext)
      this.updateContext(this.curContext.tracker.shift(this.curContext.context, term, this, this.p.stream.reset(start)));
  }
  reduceContext(term, start) {
    if (this.curContext)
      this.updateContext(this.curContext.tracker.reduce(this.curContext.context, term, this, this.p.stream.reset(start)));
  }
  /**
  @internal
  */
  emitContext() {
    let last = this.buffer.length - 1;
    if (last < 0 || this.buffer[last] != -3)
      this.buffer.push(this.curContext.hash, this.pos, this.pos, -3);
  }
  /**
  @internal
  */
  emitLookAhead() {
    let last = this.buffer.length - 1;
    if (last < 0 || this.buffer[last] != -4)
      this.buffer.push(this.lookAhead, this.pos, this.pos, -4);
  }
  updateContext(context) {
    if (context != this.curContext.context) {
      let newCx = new StackContext(this.curContext.tracker, context);
      if (newCx.hash != this.curContext.hash)
        this.emitContext();
      this.curContext = newCx;
    }
  }
  /**
  @internal
  */
  setLookAhead(lookAhead) {
    if (lookAhead <= this.lookAhead)
      return false;
    this.emitLookAhead();
    this.lookAhead = lookAhead;
    return true;
  }
  /**
  @internal
  */
  close() {
    if (this.curContext && this.curContext.tracker.strict)
      this.emitContext();
    if (this.lookAhead > 0)
      this.emitLookAhead();
  }
};
var StackContext = class {
  constructor(tracker, context) {
    this.tracker = tracker;
    this.context = context;
    this.hash = tracker.strict ? tracker.hash(context) : 0;
  }
};
var SimulatedStack = class {
  constructor(start) {
    this.start = start;
    this.state = start.state;
    this.stack = start.stack;
    this.base = this.stack.length;
  }
  reduce(action) {
    let term = action & 65535, depth = action >> 19;
    if (depth == 0) {
      if (this.stack == this.start.stack)
        this.stack = this.stack.slice();
      this.stack.push(this.state, 0, 0);
      this.base += 3;
    } else {
      this.base -= (depth - 1) * 3;
    }
    let goto = this.start.p.parser.getGoto(this.stack[this.base - 3], term, true);
    this.state = goto;
  }
};
var StackBufferCursor = class _StackBufferCursor {
  constructor(stack, pos, index) {
    this.stack = stack;
    this.pos = pos;
    this.index = index;
    this.buffer = stack.buffer;
    if (this.index == 0)
      this.maybeNext();
  }
  static create(stack, pos = stack.bufferBase + stack.buffer.length) {
    return new _StackBufferCursor(stack, pos, pos - stack.bufferBase);
  }
  maybeNext() {
    let next = this.stack.parent;
    if (next != null) {
      this.index = this.stack.bufferBase - next.bufferBase;
      this.stack = next;
      this.buffer = next.buffer;
    }
  }
  get id() {
    return this.buffer[this.index - 4];
  }
  get start() {
    return this.buffer[this.index - 3];
  }
  get end() {
    return this.buffer[this.index - 2];
  }
  get size() {
    return this.buffer[this.index - 1];
  }
  next() {
    this.index -= 4;
    this.pos -= 4;
    if (this.index == 0)
      this.maybeNext();
  }
  fork() {
    return new _StackBufferCursor(this.stack, this.pos, this.index);
  }
};
function decodeArray(input, Type = Uint16Array) {
  if (typeof input != "string")
    return input;
  let array = null;
  for (let pos = 0, out = 0; pos < input.length; ) {
    let value = 0;
    for (; ; ) {
      let next = input.charCodeAt(pos++), stop = false;
      if (next == 126) {
        value = 65535;
        break;
      }
      if (next >= 92)
        next--;
      if (next >= 34)
        next--;
      let digit = next - 32;
      if (digit >= 46) {
        digit -= 46;
        stop = true;
      }
      value += digit;
      if (stop)
        break;
      value *= 46;
    }
    if (array)
      array[out++] = value;
    else
      array = new Type(value);
  }
  return array;
}
var CachedToken = class {
  constructor() {
    this.start = -1;
    this.value = -1;
    this.end = -1;
    this.extended = -1;
    this.lookAhead = 0;
    this.mask = 0;
    this.context = 0;
  }
};
var nullToken = new CachedToken();
var InputStream = class {
  /**
  @internal
  */
  constructor(input, ranges) {
    this.input = input;
    this.ranges = ranges;
    this.chunk = "";
    this.chunkOff = 0;
    this.chunk2 = "";
    this.chunk2Pos = 0;
    this.next = -1;
    this.token = nullToken;
    this.rangeIndex = 0;
    this.pos = this.chunkPos = ranges[0].from;
    this.range = ranges[0];
    this.end = ranges[ranges.length - 1].to;
    this.readNext();
  }
  /**
  @internal
  */
  resolveOffset(offset, assoc) {
    let range = this.range, index = this.rangeIndex;
    let pos = this.pos + offset;
    while (pos < range.from) {
      if (!index)
        return null;
      let next = this.ranges[--index];
      pos -= range.from - next.to;
      range = next;
    }
    while (assoc < 0 ? pos > range.to : pos >= range.to) {
      if (index == this.ranges.length - 1)
        return null;
      let next = this.ranges[++index];
      pos += next.from - range.to;
      range = next;
    }
    return pos;
  }
  /**
  @internal
  */
  clipPos(pos) {
    if (pos >= this.range.from && pos < this.range.to)
      return pos;
    for (let range of this.ranges)
      if (range.to > pos)
        return Math.max(pos, range.from);
    return this.end;
  }
  /**
  Look at a code unit near the stream position. `.peek(0)` equals
  `.next`, `.peek(-1)` gives you the previous character, and so
  on.
  
  Note that looking around during tokenizing creates dependencies
  on potentially far-away content, which may reduce the
  effectiveness incremental parsing—when looking forward—or even
  cause invalid reparses when looking backward more than 25 code
  units, since the library does not track lookbehind.
  */
  peek(offset) {
    let idx = this.chunkOff + offset, pos, result;
    if (idx >= 0 && idx < this.chunk.length) {
      pos = this.pos + offset;
      result = this.chunk.charCodeAt(idx);
    } else {
      let resolved = this.resolveOffset(offset, 1);
      if (resolved == null)
        return -1;
      pos = resolved;
      if (pos >= this.chunk2Pos && pos < this.chunk2Pos + this.chunk2.length) {
        result = this.chunk2.charCodeAt(pos - this.chunk2Pos);
      } else {
        let i = this.rangeIndex, range = this.range;
        while (range.to <= pos)
          range = this.ranges[++i];
        this.chunk2 = this.input.chunk(this.chunk2Pos = pos);
        if (pos + this.chunk2.length > range.to)
          this.chunk2 = this.chunk2.slice(0, range.to - pos);
        result = this.chunk2.charCodeAt(0);
      }
    }
    if (pos >= this.token.lookAhead)
      this.token.lookAhead = pos + 1;
    return result;
  }
  /**
  Accept a token. By default, the end of the token is set to the
  current stream position, but you can pass an offset (relative to
  the stream position) to change that.
  */
  acceptToken(token, endOffset = 0) {
    let end = endOffset ? this.resolveOffset(endOffset, -1) : this.pos;
    if (end == null || end < this.token.start)
      throw new RangeError("Token end out of bounds");
    this.token.value = token;
    this.token.end = end;
  }
  /**
  Accept a token ending at a specific given position.
  */
  acceptTokenTo(token, endPos) {
    this.token.value = token;
    this.token.end = endPos;
  }
  getChunk() {
    if (this.pos >= this.chunk2Pos && this.pos < this.chunk2Pos + this.chunk2.length) {
      let { chunk, chunkPos } = this;
      this.chunk = this.chunk2;
      this.chunkPos = this.chunk2Pos;
      this.chunk2 = chunk;
      this.chunk2Pos = chunkPos;
      this.chunkOff = this.pos - this.chunkPos;
    } else {
      this.chunk2 = this.chunk;
      this.chunk2Pos = this.chunkPos;
      let nextChunk = this.input.chunk(this.pos);
      let end = this.pos + nextChunk.length;
      this.chunk = end > this.range.to ? nextChunk.slice(0, this.range.to - this.pos) : nextChunk;
      this.chunkPos = this.pos;
      this.chunkOff = 0;
    }
  }
  readNext() {
    if (this.chunkOff >= this.chunk.length) {
      this.getChunk();
      if (this.chunkOff == this.chunk.length)
        return this.next = -1;
    }
    return this.next = this.chunk.charCodeAt(this.chunkOff);
  }
  /**
  Move the stream forward N (defaults to 1) code units. Returns
  the new value of [`next`](#lr.InputStream.next).
  */
  advance(n = 1) {
    this.chunkOff += n;
    while (this.pos + n >= this.range.to) {
      if (this.rangeIndex == this.ranges.length - 1)
        return this.setDone();
      n -= this.range.to - this.pos;
      this.range = this.ranges[++this.rangeIndex];
      this.pos = this.range.from;
    }
    this.pos += n;
    if (this.pos >= this.token.lookAhead)
      this.token.lookAhead = this.pos + 1;
    return this.readNext();
  }
  setDone() {
    this.pos = this.chunkPos = this.end;
    this.range = this.ranges[this.rangeIndex = this.ranges.length - 1];
    this.chunk = "";
    return this.next = -1;
  }
  /**
  @internal
  */
  reset(pos, token) {
    if (token) {
      this.token = token;
      token.start = pos;
      token.lookAhead = pos + 1;
      token.value = token.extended = -1;
    } else {
      this.token = nullToken;
    }
    if (this.pos != pos) {
      this.pos = pos;
      if (pos == this.end) {
        this.setDone();
        return this;
      }
      while (pos < this.range.from)
        this.range = this.ranges[--this.rangeIndex];
      while (pos >= this.range.to)
        this.range = this.ranges[++this.rangeIndex];
      if (pos >= this.chunkPos && pos < this.chunkPos + this.chunk.length) {
        this.chunkOff = pos - this.chunkPos;
      } else {
        this.chunk = "";
        this.chunkOff = 0;
      }
      this.readNext();
    }
    return this;
  }
  /**
  @internal
  */
  read(from, to) {
    if (from >= this.chunkPos && to <= this.chunkPos + this.chunk.length)
      return this.chunk.slice(from - this.chunkPos, to - this.chunkPos);
    if (from >= this.chunk2Pos && to <= this.chunk2Pos + this.chunk2.length)
      return this.chunk2.slice(from - this.chunk2Pos, to - this.chunk2Pos);
    if (from >= this.range.from && to <= this.range.to)
      return this.input.read(from, to);
    let result = "";
    for (let r of this.ranges) {
      if (r.from >= to)
        break;
      if (r.to > from)
        result += this.input.read(Math.max(r.from, from), Math.min(r.to, to));
    }
    return result;
  }
};
var TokenGroup = class {
  constructor(data, id2) {
    this.data = data;
    this.id = id2;
  }
  token(input, stack) {
    let { parser: parser2 } = stack.p;
    readToken(this.data, input, stack, this.id, parser2.data, parser2.tokenPrecTable);
  }
};
TokenGroup.prototype.contextual = TokenGroup.prototype.fallback = TokenGroup.prototype.extend = false;
var LocalTokenGroup = class {
  constructor(data, precTable, elseToken) {
    this.precTable = precTable;
    this.elseToken = elseToken;
    this.data = typeof data == "string" ? decodeArray(data) : data;
  }
  token(input, stack) {
    let start = input.pos, skipped = 0;
    for (; ; ) {
      let atEof = input.next < 0, nextPos = input.resolveOffset(1, 1);
      readToken(this.data, input, stack, 0, this.data, this.precTable);
      if (input.token.value > -1)
        break;
      if (this.elseToken == null)
        return;
      if (!atEof)
        skipped++;
      if (nextPos == null)
        break;
      input.reset(nextPos, input.token);
    }
    if (skipped) {
      input.reset(start, input.token);
      input.acceptToken(this.elseToken, skipped);
    }
  }
};
LocalTokenGroup.prototype.contextual = TokenGroup.prototype.fallback = TokenGroup.prototype.extend = false;
var ExternalTokenizer = class {
  /**
  Create a tokenizer. The first argument is the function that,
  given an input stream, scans for the types of tokens it
  recognizes at the stream's position, and calls
  [`acceptToken`](#lr.InputStream.acceptToken) when it finds
  one.
  */
  constructor(token, options = {}) {
    this.token = token;
    this.contextual = !!options.contextual;
    this.fallback = !!options.fallback;
    this.extend = !!options.extend;
  }
};
function readToken(data, input, stack, group, precTable, precOffset) {
  let state = 0, groupMask = 1 << group, { dialect } = stack.p.parser;
  scan: for (; ; ) {
    if ((groupMask & data[state]) == 0)
      break;
    let accEnd = data[state + 1];
    for (let i = state + 3; i < accEnd; i += 2)
      if ((data[i + 1] & groupMask) > 0) {
        let term = data[i];
        if (dialect.allows(term) && (input.token.value == -1 || input.token.value == term || overrides(term, input.token.value, precTable, precOffset))) {
          input.acceptToken(term);
          break;
        }
      }
    let next = input.next, low = 0, high = data[state + 2];
    if (input.next < 0 && high > low && data[accEnd + high * 3 - 3] == 65535) {
      state = data[accEnd + high * 3 - 1];
      continue scan;
    }
    for (; low < high; ) {
      let mid = low + high >> 1;
      let index = accEnd + mid + (mid << 1);
      let from = data[index], to = data[index + 1] || 65536;
      if (next < from)
        high = mid;
      else if (next >= to)
        low = mid + 1;
      else {
        state = data[index + 2];
        input.advance();
        continue scan;
      }
    }
    break;
  }
}
function findOffset(data, start, term) {
  for (let i = start, next; (next = data[i]) != 65535; i++)
    if (next == term)
      return i - start;
  return -1;
}
function overrides(token, prev, tableData, tableOffset) {
  let iPrev = findOffset(tableData, tableOffset, prev);
  return iPrev < 0 || findOffset(tableData, tableOffset, token) < iPrev;
}
var verbose = typeof process != "undefined" && process.env && /\bparse\b/.test(process.env.LOG);
var stackIDs = null;
function cutAt(tree, pos, side) {
  let cursor = tree.cursor(IterMode.IncludeAnonymous);
  cursor.moveTo(pos);
  for (; ; ) {
    if (!(side < 0 ? cursor.childBefore(pos) : cursor.childAfter(pos)))
      for (; ; ) {
        if ((side < 0 ? cursor.to < pos : cursor.from > pos) && !cursor.type.isError)
          return side < 0 ? Math.max(0, Math.min(
            cursor.to - 1,
            pos - 25
            /* Lookahead.Margin */
          )) : Math.min(tree.length, Math.max(
            cursor.from + 1,
            pos + 25
            /* Lookahead.Margin */
          ));
        if (side < 0 ? cursor.prevSibling() : cursor.nextSibling())
          break;
        if (!cursor.parent())
          return side < 0 ? 0 : tree.length;
      }
  }
}
var FragmentCursor = class {
  constructor(fragments, nodeSet) {
    this.fragments = fragments;
    this.nodeSet = nodeSet;
    this.i = 0;
    this.fragment = null;
    this.safeFrom = -1;
    this.safeTo = -1;
    this.trees = [];
    this.start = [];
    this.index = [];
    this.nextFragment();
  }
  nextFragment() {
    let fr = this.fragment = this.i == this.fragments.length ? null : this.fragments[this.i++];
    if (fr) {
      this.safeFrom = fr.openStart ? cutAt(fr.tree, fr.from + fr.offset, 1) - fr.offset : fr.from;
      this.safeTo = fr.openEnd ? cutAt(fr.tree, fr.to + fr.offset, -1) - fr.offset : fr.to;
      while (this.trees.length) {
        this.trees.pop();
        this.start.pop();
        this.index.pop();
      }
      this.trees.push(fr.tree);
      this.start.push(-fr.offset);
      this.index.push(0);
      this.nextStart = this.safeFrom;
    } else {
      this.nextStart = 1e9;
    }
  }
  // `pos` must be >= any previously given `pos` for this cursor
  nodeAt(pos) {
    if (pos < this.nextStart)
      return null;
    while (this.fragment && this.safeTo <= pos)
      this.nextFragment();
    if (!this.fragment)
      return null;
    for (; ; ) {
      let last = this.trees.length - 1;
      if (last < 0) {
        this.nextFragment();
        return null;
      }
      let top = this.trees[last], index = this.index[last];
      if (index == top.children.length) {
        this.trees.pop();
        this.start.pop();
        this.index.pop();
        continue;
      }
      let next = top.children[index];
      let start = this.start[last] + top.positions[index];
      if (start > pos) {
        this.nextStart = start;
        return null;
      }
      if (next instanceof Tree) {
        if (start == pos) {
          if (start < this.safeFrom)
            return null;
          let end = start + next.length;
          if (end <= this.safeTo) {
            let lookAhead = next.prop(NodeProp.lookAhead);
            if (!lookAhead || end + lookAhead < this.fragment.to)
              return next;
          }
        }
        this.index[last]++;
        if (start + next.length >= Math.max(this.safeFrom, pos)) {
          this.trees.push(next);
          this.start.push(start);
          this.index.push(0);
        }
      } else {
        this.index[last]++;
        this.nextStart = start + next.length;
      }
    }
  }
};
var TokenCache = class {
  constructor(parser2, stream) {
    this.stream = stream;
    this.tokens = [];
    this.mainToken = null;
    this.actions = [];
    this.tokens = parser2.tokenizers.map((_) => new CachedToken());
  }
  getActions(stack) {
    let actionIndex = 0;
    let main = null;
    let { parser: parser2 } = stack.p, { tokenizers } = parser2;
    let mask = parser2.stateSlot(
      stack.state,
      3
      /* ParseState.TokenizerMask */
    );
    let context = stack.curContext ? stack.curContext.hash : 0;
    let lookAhead = 0;
    for (let i = 0; i < tokenizers.length; i++) {
      if ((1 << i & mask) == 0)
        continue;
      let tokenizer = tokenizers[i], token = this.tokens[i];
      if (main && !tokenizer.fallback)
        continue;
      if (tokenizer.contextual || token.start != stack.pos || token.mask != mask || token.context != context) {
        this.updateCachedToken(token, tokenizer, stack);
        token.mask = mask;
        token.context = context;
      }
      if (token.lookAhead > token.end + 25)
        lookAhead = Math.max(token.lookAhead, lookAhead);
      if (token.value != 0) {
        let startIndex = actionIndex;
        if (token.extended > -1)
          actionIndex = this.addActions(stack, token.extended, token.end, actionIndex);
        actionIndex = this.addActions(stack, token.value, token.end, actionIndex);
        if (!tokenizer.extend) {
          main = token;
          if (actionIndex > startIndex)
            break;
        }
      }
    }
    while (this.actions.length > actionIndex)
      this.actions.pop();
    if (lookAhead)
      stack.setLookAhead(lookAhead);
    if (!main && stack.pos == this.stream.end) {
      main = new CachedToken();
      main.value = stack.p.parser.eofTerm;
      main.start = main.end = stack.pos;
      actionIndex = this.addActions(stack, main.value, main.end, actionIndex);
    }
    this.mainToken = main;
    return this.actions;
  }
  getMainToken(stack) {
    if (this.mainToken)
      return this.mainToken;
    let main = new CachedToken(), { pos, p } = stack;
    main.start = pos;
    main.end = Math.min(pos + 1, p.stream.end);
    main.value = pos == p.stream.end ? p.parser.eofTerm : 0;
    return main;
  }
  updateCachedToken(token, tokenizer, stack) {
    let start = this.stream.clipPos(stack.pos);
    tokenizer.token(this.stream.reset(start, token), stack);
    if (token.value > -1) {
      let { parser: parser2 } = stack.p;
      for (let i = 0; i < parser2.specialized.length; i++)
        if (parser2.specialized[i] == token.value) {
          let result = parser2.specializers[i](this.stream.read(token.start, token.end), stack);
          if (result >= 0 && stack.p.parser.dialect.allows(result >> 1)) {
            if ((result & 1) == 0)
              token.value = result >> 1;
            else
              token.extended = result >> 1;
            break;
          }
        }
    } else {
      token.value = 0;
      token.end = this.stream.clipPos(start + 1);
    }
  }
  putAction(action, token, end, index) {
    for (let i = 0; i < index; i += 3)
      if (this.actions[i] == action)
        return index;
    this.actions[index++] = action;
    this.actions[index++] = token;
    this.actions[index++] = end;
    return index;
  }
  addActions(stack, token, end, index) {
    let { state } = stack, { parser: parser2 } = stack.p, { data } = parser2;
    for (let set = 0; set < 2; set++) {
      for (let i = parser2.stateSlot(
        state,
        set ? 2 : 1
        /* ParseState.Actions */
      ); ; i += 3) {
        if (data[i] == 65535) {
          if (data[i + 1] == 1) {
            i = pair(data, i + 2);
          } else {
            if (index == 0 && data[i + 1] == 2)
              index = this.putAction(pair(data, i + 2), token, end, index);
            break;
          }
        }
        if (data[i] == token)
          index = this.putAction(pair(data, i + 1), token, end, index);
      }
    }
    return index;
  }
};
var Parse = class {
  constructor(parser2, input, fragments, ranges) {
    this.parser = parser2;
    this.input = input;
    this.ranges = ranges;
    this.recovering = 0;
    this.nextStackID = 9812;
    this.minStackPos = 0;
    this.reused = [];
    this.stoppedAt = null;
    this.lastBigReductionStart = -1;
    this.lastBigReductionSize = 0;
    this.bigReductionCount = 0;
    this.stream = new InputStream(input, ranges);
    this.tokens = new TokenCache(parser2, this.stream);
    this.topTerm = parser2.top[1];
    let { from } = ranges[0];
    this.stacks = [Stack.start(this, parser2.top[0], from)];
    this.fragments = fragments.length && this.stream.end - from > parser2.bufferLength * 4 ? new FragmentCursor(fragments, parser2.nodeSet) : null;
  }
  get parsedPos() {
    return this.minStackPos;
  }
  // Move the parser forward. This will process all parse stacks at
  // `this.pos` and try to advance them to a further position. If no
  // stack for such a position is found, it'll start error-recovery.
  //
  // When the parse is finished, this will return a syntax tree. When
  // not, it returns `null`.
  advance() {
    let stacks = this.stacks, pos = this.minStackPos;
    let newStacks = this.stacks = [];
    let stopped, stoppedTokens;
    if (this.bigReductionCount > 300 && stacks.length == 1) {
      let [s] = stacks;
      while (s.forceReduce() && s.stack.length && s.stack[s.stack.length - 2] >= this.lastBigReductionStart) {
      }
      this.bigReductionCount = this.lastBigReductionSize = 0;
    }
    for (let i = 0; i < stacks.length; i++) {
      let stack = stacks[i];
      for (; ; ) {
        this.tokens.mainToken = null;
        if (stack.pos > pos) {
          newStacks.push(stack);
        } else if (this.advanceStack(stack, newStacks, stacks)) {
          continue;
        } else {
          if (!stopped) {
            stopped = [];
            stoppedTokens = [];
          }
          stopped.push(stack);
          let tok = this.tokens.getMainToken(stack);
          stoppedTokens.push(tok.value, tok.end);
        }
        break;
      }
    }
    if (!newStacks.length) {
      let finished = stopped && findFinished(stopped);
      if (finished) {
        if (verbose)
          console.log("Finish with " + this.stackID(finished));
        return this.stackToTree(finished);
      }
      if (this.parser.strict) {
        if (verbose && stopped)
          console.log("Stuck with token " + (this.tokens.mainToken ? this.parser.getName(this.tokens.mainToken.value) : "none"));
        throw new SyntaxError("No parse at " + pos);
      }
      if (!this.recovering)
        this.recovering = 5;
    }
    if (this.recovering && stopped) {
      let finished = this.stoppedAt != null && stopped[0].pos > this.stoppedAt ? stopped[0] : this.runRecovery(stopped, stoppedTokens, newStacks);
      if (finished) {
        if (verbose)
          console.log("Force-finish " + this.stackID(finished));
        return this.stackToTree(finished.forceAll());
      }
    }
    if (this.recovering) {
      let maxRemaining = this.recovering == 1 ? 1 : this.recovering * 3;
      if (newStacks.length > maxRemaining) {
        newStacks.sort((a, b) => b.score - a.score);
        while (newStacks.length > maxRemaining)
          newStacks.pop();
      }
      if (newStacks.some((s) => s.reducePos > pos))
        this.recovering--;
    } else if (newStacks.length > 1) {
      outer: for (let i = 0; i < newStacks.length - 1; i++) {
        let stack = newStacks[i];
        for (let j = i + 1; j < newStacks.length; j++) {
          let other = newStacks[j];
          if (stack.sameState(other) || stack.buffer.length > 500 && other.buffer.length > 500) {
            if ((stack.score - other.score || stack.buffer.length - other.buffer.length) > 0) {
              newStacks.splice(j--, 1);
            } else {
              newStacks.splice(i--, 1);
              continue outer;
            }
          }
        }
      }
      if (newStacks.length > 12) {
        newStacks.sort((a, b) => b.score - a.score);
        newStacks.splice(
          12,
          newStacks.length - 12
          /* Rec.MaxStackCount */
        );
      }
    }
    this.minStackPos = newStacks[0].pos;
    for (let i = 1; i < newStacks.length; i++)
      if (newStacks[i].pos < this.minStackPos)
        this.minStackPos = newStacks[i].pos;
    return null;
  }
  stopAt(pos) {
    if (this.stoppedAt != null && this.stoppedAt < pos)
      throw new RangeError("Can't move stoppedAt forward");
    this.stoppedAt = pos;
  }
  // Returns an updated version of the given stack, or null if the
  // stack can't advance normally. When `split` and `stacks` are
  // given, stacks split off by ambiguous operations will be pushed to
  // `split`, or added to `stacks` if they move `pos` forward.
  advanceStack(stack, stacks, split) {
    let start = stack.pos, { parser: parser2 } = this;
    let base = verbose ? this.stackID(stack) + " -> " : "";
    if (this.stoppedAt != null && start > this.stoppedAt)
      return stack.forceReduce() ? stack : null;
    if (this.fragments) {
      let strictCx = stack.curContext && stack.curContext.tracker.strict, cxHash = strictCx ? stack.curContext.hash : 0;
      for (let cached = this.fragments.nodeAt(start); cached; ) {
        let match = this.parser.nodeSet.types[cached.type.id] == cached.type ? parser2.getGoto(stack.state, cached.type.id) : -1;
        if (match > -1 && cached.length && (!strictCx || (cached.prop(NodeProp.contextHash) || 0) == cxHash)) {
          stack.useNode(cached, match);
          if (verbose)
            console.log(base + this.stackID(stack) + ` (via reuse of ${parser2.getName(cached.type.id)})`);
          return true;
        }
        if (!(cached instanceof Tree) || cached.children.length == 0 || cached.positions[0] > 0)
          break;
        let inner = cached.children[0];
        if (inner instanceof Tree && cached.positions[0] == 0)
          cached = inner;
        else
          break;
      }
    }
    let defaultReduce = parser2.stateSlot(
      stack.state,
      4
      /* ParseState.DefaultReduce */
    );
    if (defaultReduce > 0) {
      stack.reduce(defaultReduce);
      if (verbose)
        console.log(base + this.stackID(stack) + ` (via always-reduce ${parser2.getName(
          defaultReduce & 65535
          /* Action.ValueMask */
        )})`);
      return true;
    }
    if (stack.stack.length >= 8400) {
      while (stack.stack.length > 6e3 && stack.forceReduce()) {
      }
    }
    let actions = this.tokens.getActions(stack);
    for (let i = 0; i < actions.length; ) {
      let action = actions[i++], term = actions[i++], end = actions[i++];
      let last = i == actions.length || !split;
      let localStack = last ? stack : stack.split();
      let main = this.tokens.mainToken;
      localStack.apply(action, term, main ? main.start : localStack.pos, end);
      if (verbose)
        console.log(base + this.stackID(localStack) + ` (via ${(action & 65536) == 0 ? "shift" : `reduce of ${parser2.getName(
          action & 65535
          /* Action.ValueMask */
        )}`} for ${parser2.getName(term)} @ ${start}${localStack == stack ? "" : ", split"})`);
      if (last)
        return true;
      else if (localStack.pos > start)
        stacks.push(localStack);
      else
        split.push(localStack);
    }
    return false;
  }
  // Advance a given stack forward as far as it will go. Returns the
  // (possibly updated) stack if it got stuck, or null if it moved
  // forward and was given to `pushStackDedup`.
  advanceFully(stack, newStacks) {
    let pos = stack.pos;
    for (; ; ) {
      if (!this.advanceStack(stack, null, null))
        return false;
      if (stack.pos > pos) {
        pushStackDedup(stack, newStacks);
        return true;
      }
    }
  }
  runRecovery(stacks, tokens, newStacks) {
    let finished = null, restarted = false;
    for (let i = 0; i < stacks.length; i++) {
      let stack = stacks[i], token = tokens[i << 1], tokenEnd = tokens[(i << 1) + 1];
      let base = verbose ? this.stackID(stack) + " -> " : "";
      if (stack.deadEnd) {
        if (restarted)
          continue;
        restarted = true;
        stack.restart();
        if (verbose)
          console.log(base + this.stackID(stack) + " (restarted)");
        let done = this.advanceFully(stack, newStacks);
        if (done)
          continue;
      }
      let force = stack.split(), forceBase = base;
      for (let j = 0; j < 10 && force.forceReduce(); j++) {
        if (verbose)
          console.log(forceBase + this.stackID(force) + " (via force-reduce)");
        let done = this.advanceFully(force, newStacks);
        if (done)
          break;
        if (verbose)
          forceBase = this.stackID(force) + " -> ";
      }
      for (let insert of stack.recoverByInsert(token)) {
        if (verbose)
          console.log(base + this.stackID(insert) + " (via recover-insert)");
        this.advanceFully(insert, newStacks);
      }
      if (this.stream.end > stack.pos) {
        if (tokenEnd == stack.pos) {
          tokenEnd++;
          token = 0;
        }
        stack.recoverByDelete(token, tokenEnd);
        if (verbose)
          console.log(base + this.stackID(stack) + ` (via recover-delete ${this.parser.getName(token)})`);
        pushStackDedup(stack, newStacks);
      } else if (!finished || finished.score < force.score) {
        finished = force;
      }
    }
    return finished;
  }
  // Convert the stack's buffer to a syntax tree.
  stackToTree(stack) {
    stack.close();
    return Tree.build({
      buffer: StackBufferCursor.create(stack),
      nodeSet: this.parser.nodeSet,
      topID: this.topTerm,
      maxBufferLength: this.parser.bufferLength,
      reused: this.reused,
      start: this.ranges[0].from,
      length: stack.pos - this.ranges[0].from,
      minRepeatType: this.parser.minRepeatTerm
    });
  }
  stackID(stack) {
    let id2 = (stackIDs || (stackIDs = /* @__PURE__ */ new WeakMap())).get(stack);
    if (!id2)
      stackIDs.set(stack, id2 = String.fromCodePoint(this.nextStackID++));
    return id2 + stack;
  }
};
function pushStackDedup(stack, newStacks) {
  for (let i = 0; i < newStacks.length; i++) {
    let other = newStacks[i];
    if (other.pos == stack.pos && other.sameState(stack)) {
      if (newStacks[i].score < stack.score)
        newStacks[i] = stack;
      return;
    }
  }
  newStacks.push(stack);
}
var Dialect = class {
  constructor(source, flags, disabled) {
    this.source = source;
    this.flags = flags;
    this.disabled = disabled;
  }
  allows(term) {
    return !this.disabled || this.disabled[term] == 0;
  }
};
var id = (x) => x;
var ContextTracker = class {
  /**
  Define a context tracker.
  */
  constructor(spec) {
    this.start = spec.start;
    this.shift = spec.shift || id;
    this.reduce = spec.reduce || id;
    this.reuse = spec.reuse || id;
    this.hash = spec.hash || (() => 0);
    this.strict = spec.strict !== false;
  }
};
var LRParser = class _LRParser extends Parser {
  /**
  @internal
  */
  constructor(spec) {
    super();
    this.wrappers = [];
    if (spec.version != 14)
      throw new RangeError(`Parser version (${spec.version}) doesn't match runtime version (${14})`);
    let nodeNames = spec.nodeNames.split(" ");
    this.minRepeatTerm = nodeNames.length;
    for (let i = 0; i < spec.repeatNodeCount; i++)
      nodeNames.push("");
    let topTerms = Object.keys(spec.topRules).map((r) => spec.topRules[r][1]);
    let nodeProps = [];
    for (let i = 0; i < nodeNames.length; i++)
      nodeProps.push([]);
    function setProp(nodeID, prop, value) {
      nodeProps[nodeID].push([prop, prop.deserialize(String(value))]);
    }
    if (spec.nodeProps)
      for (let propSpec of spec.nodeProps) {
        let prop = propSpec[0];
        if (typeof prop == "string")
          prop = NodeProp[prop];
        for (let i = 1; i < propSpec.length; ) {
          let next = propSpec[i++];
          if (next >= 0) {
            setProp(next, prop, propSpec[i++]);
          } else {
            let value = propSpec[i + -next];
            for (let j = -next; j > 0; j--)
              setProp(propSpec[i++], prop, value);
            i++;
          }
        }
      }
    this.nodeSet = new NodeSet(nodeNames.map((name2, i) => NodeType.define({
      name: i >= this.minRepeatTerm ? void 0 : name2,
      id: i,
      props: nodeProps[i],
      top: topTerms.indexOf(i) > -1,
      error: i == 0,
      skipped: spec.skippedNodes && spec.skippedNodes.indexOf(i) > -1
    })));
    if (spec.propSources)
      this.nodeSet = this.nodeSet.extend(...spec.propSources);
    this.strict = false;
    this.bufferLength = DefaultBufferLength;
    let tokenArray = decodeArray(spec.tokenData);
    this.context = spec.context;
    this.specializerSpecs = spec.specialized || [];
    this.specialized = new Uint16Array(this.specializerSpecs.length);
    for (let i = 0; i < this.specializerSpecs.length; i++)
      this.specialized[i] = this.specializerSpecs[i].term;
    this.specializers = this.specializerSpecs.map(getSpecializer);
    this.states = decodeArray(spec.states, Uint32Array);
    this.data = decodeArray(spec.stateData);
    this.goto = decodeArray(spec.goto);
    this.maxTerm = spec.maxTerm;
    this.tokenizers = spec.tokenizers.map((value) => typeof value == "number" ? new TokenGroup(tokenArray, value) : value);
    this.topRules = spec.topRules;
    this.dialects = spec.dialects || {};
    this.dynamicPrecedences = spec.dynamicPrecedences || null;
    this.tokenPrecTable = spec.tokenPrec;
    this.termNames = spec.termNames || null;
    this.maxNode = this.nodeSet.types.length - 1;
    this.dialect = this.parseDialect();
    this.top = this.topRules[Object.keys(this.topRules)[0]];
  }
  createParse(input, fragments, ranges) {
    let parse = new Parse(this, input, fragments, ranges);
    for (let w of this.wrappers)
      parse = w(parse, input, fragments, ranges);
    return parse;
  }
  /**
  Get a goto table entry @internal
  */
  getGoto(state, term, loose = false) {
    let table = this.goto;
    if (term >= table[0])
      return -1;
    for (let pos = table[term + 1]; ; ) {
      let groupTag = table[pos++], last = groupTag & 1;
      let target = table[pos++];
      if (last && loose)
        return target;
      for (let end = pos + (groupTag >> 1); pos < end; pos++)
        if (table[pos] == state)
          return target;
      if (last)
        return -1;
    }
  }
  /**
  Check if this state has an action for a given terminal @internal
  */
  hasAction(state, terminal) {
    let data = this.data;
    for (let set = 0; set < 2; set++) {
      for (let i = this.stateSlot(
        state,
        set ? 2 : 1
        /* ParseState.Actions */
      ), next; ; i += 3) {
        if ((next = data[i]) == 65535) {
          if (data[i + 1] == 1)
            next = data[i = pair(data, i + 2)];
          else if (data[i + 1] == 2)
            return pair(data, i + 2);
          else
            break;
        }
        if (next == terminal || next == 0)
          return pair(data, i + 1);
      }
    }
    return 0;
  }
  /**
  @internal
  */
  stateSlot(state, slot) {
    return this.states[state * 6 + slot];
  }
  /**
  @internal
  */
  stateFlag(state, flag) {
    return (this.stateSlot(
      state,
      0
      /* ParseState.Flags */
    ) & flag) > 0;
  }
  /**
  @internal
  */
  validAction(state, action) {
    return !!this.allActions(state, (a) => a == action ? true : null);
  }
  /**
  @internal
  */
  allActions(state, action) {
    let deflt = this.stateSlot(
      state,
      4
      /* ParseState.DefaultReduce */
    );
    let result = deflt ? action(deflt) : void 0;
    for (let i = this.stateSlot(
      state,
      1
      /* ParseState.Actions */
    ); result == null; i += 3) {
      if (this.data[i] == 65535) {
        if (this.data[i + 1] == 1)
          i = pair(this.data, i + 2);
        else
          break;
      }
      result = action(pair(this.data, i + 1));
    }
    return result;
  }
  /**
  Get the states that can follow this one through shift actions or
  goto jumps. @internal
  */
  nextStates(state) {
    let result = [];
    for (let i = this.stateSlot(
      state,
      1
      /* ParseState.Actions */
    ); ; i += 3) {
      if (this.data[i] == 65535) {
        if (this.data[i + 1] == 1)
          i = pair(this.data, i + 2);
        else
          break;
      }
      if ((this.data[i + 2] & 65536 >> 16) == 0) {
        let value = this.data[i + 1];
        if (!result.some((v, i2) => i2 & 1 && v == value))
          result.push(this.data[i], value);
      }
    }
    return result;
  }
  /**
  Configure the parser. Returns a new parser instance that has the
  given settings modified. Settings not provided in `config` are
  kept from the original parser.
  */
  configure(config) {
    let copy = Object.assign(Object.create(_LRParser.prototype), this);
    if (config.props)
      copy.nodeSet = this.nodeSet.extend(...config.props);
    if (config.top) {
      let info = this.topRules[config.top];
      if (!info)
        throw new RangeError(`Invalid top rule name ${config.top}`);
      copy.top = info;
    }
    if (config.tokenizers)
      copy.tokenizers = this.tokenizers.map((t2) => {
        let found = config.tokenizers.find((r) => r.from == t2);
        return found ? found.to : t2;
      });
    if (config.specializers) {
      copy.specializers = this.specializers.slice();
      copy.specializerSpecs = this.specializerSpecs.map((s, i) => {
        let found = config.specializers.find((r) => r.from == s.external);
        if (!found)
          return s;
        let spec = Object.assign(Object.assign({}, s), { external: found.to });
        copy.specializers[i] = getSpecializer(spec);
        return spec;
      });
    }
    if (config.contextTracker)
      copy.context = config.contextTracker;
    if (config.dialect)
      copy.dialect = this.parseDialect(config.dialect);
    if (config.strict != null)
      copy.strict = config.strict;
    if (config.wrap)
      copy.wrappers = copy.wrappers.concat(config.wrap);
    if (config.bufferLength != null)
      copy.bufferLength = config.bufferLength;
    return copy;
  }
  /**
  Tells you whether any [parse wrappers](#lr.ParserConfig.wrap)
  are registered for this parser.
  */
  hasWrappers() {
    return this.wrappers.length > 0;
  }
  /**
  Returns the name associated with a given term. This will only
  work for all terms when the parser was generated with the
  `--names` option. By default, only the names of tagged terms are
  stored.
  */
  getName(term) {
    return this.termNames ? this.termNames[term] : String(term <= this.maxNode && this.nodeSet.types[term].name || term);
  }
  /**
  The eof term id is always allocated directly after the node
  types. @internal
  */
  get eofTerm() {
    return this.maxNode + 1;
  }
  /**
  The type of top node produced by the parser.
  */
  get topNode() {
    return this.nodeSet.types[this.top[1]];
  }
  /**
  @internal
  */
  dynamicPrecedence(term) {
    let prec = this.dynamicPrecedences;
    return prec == null ? 0 : prec[term] || 0;
  }
  /**
  @internal
  */
  parseDialect(dialect) {
    let values = Object.keys(this.dialects), flags = values.map(() => false);
    if (dialect)
      for (let part of dialect.split(" ")) {
        let id2 = values.indexOf(part);
        if (id2 >= 0)
          flags[id2] = true;
      }
    let disabled = null;
    for (let i = 0; i < values.length; i++)
      if (!flags[i]) {
        for (let j = this.dialects[values[i]], id2; (id2 = this.data[j++]) != 65535; )
          (disabled || (disabled = new Uint8Array(this.maxTerm + 1)))[id2] = 1;
      }
    return new Dialect(dialect, flags, disabled);
  }
  /**
  Used by the output of the parser generator. Not available to
  user code. @hide
  */
  static deserialize(spec) {
    return new _LRParser(spec);
  }
};
function pair(data, off) {
  return data[off] | data[off + 1] << 16;
}
function findFinished(stacks) {
  let best = null;
  for (let stack of stacks) {
    let stopped = stack.p.stoppedAt;
    if ((stack.pos == stack.p.stream.end || stopped != null && stack.pos > stopped) && stack.p.parser.stateFlag(
      stack.state,
      2
      /* StateFlag.Accepting */
    ) && (!best || best.score < stack.score))
      best = stack;
  }
  return best;
}
function getSpecializer(spec) {
  if (spec.external) {
    let mask = spec.extend ? 1 : 0;
    return (value, stack) => spec.external(value, stack) << 1 | mask;
  }
  return spec.get;
}

// node_modules/@lezer/highlight/dist/index.js
var nextTagID = 0;
var Tag = class _Tag {
  /**
  @internal
  */
  constructor(name2, set, base, modified) {
    this.name = name2;
    this.set = set;
    this.base = base;
    this.modified = modified;
    this.id = nextTagID++;
  }
  toString() {
    let { name: name2 } = this;
    for (let mod of this.modified)
      if (mod.name)
        name2 = `${mod.name}(${name2})`;
    return name2;
  }
  static define(nameOrParent, parent) {
    let name2 = typeof nameOrParent == "string" ? nameOrParent : "?";
    if (nameOrParent instanceof _Tag)
      parent = nameOrParent;
    if (parent === null || parent === void 0 ? void 0 : parent.base)
      throw new Error("Can not derive from a modified tag");
    let tag = new _Tag(name2, [], null, []);
    tag.set.push(tag);
    if (parent)
      for (let t2 of parent.set)
        tag.set.push(t2);
    return tag;
  }
  /**
  Define a tag _modifier_, which is a function that, given a tag,
  will return a tag that is a subtag of the original. Applying the
  same modifier to a twice tag will return the same value (`m1(t1)
  == m1(t1)`) and applying multiple modifiers will, regardless or
  order, produce the same tag (`m1(m2(t1)) == m2(m1(t1))`).
  
  When multiple modifiers are applied to a given base tag, each
  smaller set of modifiers is registered as a parent, so that for
  example `m1(m2(m3(t1)))` is a subtype of `m1(m2(t1))`,
  `m1(m3(t1)`, and so on.
  */
  static defineModifier(name2) {
    let mod = new Modifier(name2);
    return (tag) => {
      if (tag.modified.indexOf(mod) > -1)
        return tag;
      return Modifier.get(tag.base || tag, tag.modified.concat(mod).sort((a, b) => a.id - b.id));
    };
  }
};
var nextModifierID = 0;
var Modifier = class _Modifier {
  constructor(name2) {
    this.name = name2;
    this.instances = [];
    this.id = nextModifierID++;
  }
  static get(base, mods) {
    if (!mods.length)
      return base;
    let exists = mods[0].instances.find((t2) => t2.base == base && sameArray(mods, t2.modified));
    if (exists)
      return exists;
    let set = [], tag = new Tag(base.name, set, base, mods);
    for (let m of mods)
      m.instances.push(tag);
    let configs = powerSet(mods);
    for (let parent of base.set)
      if (!parent.modified.length)
        for (let config of configs)
          set.push(_Modifier.get(parent, config));
    return tag;
  }
};
function sameArray(a, b) {
  return a.length == b.length && a.every((x, i) => x == b[i]);
}
function powerSet(array) {
  let sets = [[]];
  for (let i = 0; i < array.length; i++) {
    for (let j = 0, e = sets.length; j < e; j++) {
      sets.push(sets[j].concat(array[i]));
    }
  }
  return sets.sort((a, b) => b.length - a.length);
}
function styleTags(spec) {
  let byName = /* @__PURE__ */ Object.create(null);
  for (let prop in spec) {
    let tags2 = spec[prop];
    if (!Array.isArray(tags2))
      tags2 = [tags2];
    for (let part of prop.split(" "))
      if (part) {
        let pieces = [], mode = 2, rest = part;
        for (let pos = 0; ; ) {
          if (rest == "..." && pos > 0 && pos + 3 == part.length) {
            mode = 1;
            break;
          }
          let m = /^"(?:[^"\\]|\\.)*?"|[^\/!]+/.exec(rest);
          if (!m)
            throw new RangeError("Invalid path: " + part);
          pieces.push(m[0] == "*" ? "" : m[0][0] == '"' ? JSON.parse(m[0]) : m[0]);
          pos += m[0].length;
          if (pos == part.length)
            break;
          let next = part[pos++];
          if (pos == part.length && next == "!") {
            mode = 0;
            break;
          }
          if (next != "/")
            throw new RangeError("Invalid path: " + part);
          rest = part.slice(pos);
        }
        let last = pieces.length - 1, inner = pieces[last];
        if (!inner)
          throw new RangeError("Invalid path: " + part);
        let rule = new Rule(tags2, mode, last > 0 ? pieces.slice(0, last) : null);
        byName[inner] = rule.sort(byName[inner]);
      }
  }
  return ruleNodeProp.add(byName);
}
var ruleNodeProp = new NodeProp({
  combine(a, b) {
    let cur, root, take;
    while (a || b) {
      if (!a || b && a.depth >= b.depth) {
        take = b;
        b = b.next;
      } else {
        take = a;
        a = a.next;
      }
      if (cur && cur.mode == take.mode && !take.context && !cur.context)
        continue;
      let copy = new Rule(take.tags, take.mode, take.context);
      if (cur)
        cur.next = copy;
      else
        root = copy;
      cur = copy;
    }
    return root;
  }
});
var Rule = class {
  constructor(tags2, mode, context, next) {
    this.tags = tags2;
    this.mode = mode;
    this.context = context;
    this.next = next;
  }
  get opaque() {
    return this.mode == 0;
  }
  get inherit() {
    return this.mode == 1;
  }
  sort(other) {
    if (!other || other.depth < this.depth) {
      this.next = other;
      return this;
    }
    other.next = this.sort(other.next);
    return other;
  }
  get depth() {
    return this.context ? this.context.length : 0;
  }
};
Rule.empty = new Rule([], 2, null);
function tagHighlighter(tags2, options) {
  let map = /* @__PURE__ */ Object.create(null);
  for (let style of tags2) {
    if (!Array.isArray(style.tag))
      map[style.tag.id] = style.class;
    else
      for (let tag of style.tag)
        map[tag.id] = style.class;
  }
  let { scope, all = null } = options || {};
  return {
    style: (tags3) => {
      let cls = all;
      for (let tag of tags3) {
        for (let sub of tag.set) {
          let tagClass = map[sub.id];
          if (tagClass) {
            cls = cls ? cls + " " + tagClass : tagClass;
            break;
          }
        }
      }
      return cls;
    },
    scope
  };
}
var t = Tag.define;
var comment = t();
var name = t();
var typeName = t(name);
var propertyName = t(name);
var literal = t();
var string = t(literal);
var number = t(literal);
var content = t();
var heading = t(content);
var keyword = t();
var operator = t();
var punctuation = t();
var bracket = t(punctuation);
var meta = t();
var tags = {
  /**
  A comment.
  */
  comment,
  /**
  A line [comment](#highlight.tags.comment).
  */
  lineComment: t(comment),
  /**
  A block [comment](#highlight.tags.comment).
  */
  blockComment: t(comment),
  /**
  A documentation [comment](#highlight.tags.comment).
  */
  docComment: t(comment),
  /**
  Any kind of identifier.
  */
  name,
  /**
  The [name](#highlight.tags.name) of a variable.
  */
  variableName: t(name),
  /**
  A type [name](#highlight.tags.name).
  */
  typeName,
  /**
  A tag name (subtag of [`typeName`](#highlight.tags.typeName)).
  */
  tagName: t(typeName),
  /**
  A property or field [name](#highlight.tags.name).
  */
  propertyName,
  /**
  An attribute name (subtag of [`propertyName`](#highlight.tags.propertyName)).
  */
  attributeName: t(propertyName),
  /**
  The [name](#highlight.tags.name) of a class.
  */
  className: t(name),
  /**
  A label [name](#highlight.tags.name).
  */
  labelName: t(name),
  /**
  A namespace [name](#highlight.tags.name).
  */
  namespace: t(name),
  /**
  The [name](#highlight.tags.name) of a macro.
  */
  macroName: t(name),
  /**
  A literal value.
  */
  literal,
  /**
  A string [literal](#highlight.tags.literal).
  */
  string,
  /**
  A documentation [string](#highlight.tags.string).
  */
  docString: t(string),
  /**
  A character literal (subtag of [string](#highlight.tags.string)).
  */
  character: t(string),
  /**
  An attribute value (subtag of [string](#highlight.tags.string)).
  */
  attributeValue: t(string),
  /**
  A number [literal](#highlight.tags.literal).
  */
  number,
  /**
  An integer [number](#highlight.tags.number) literal.
  */
  integer: t(number),
  /**
  A floating-point [number](#highlight.tags.number) literal.
  */
  float: t(number),
  /**
  A boolean [literal](#highlight.tags.literal).
  */
  bool: t(literal),
  /**
  Regular expression [literal](#highlight.tags.literal).
  */
  regexp: t(literal),
  /**
  An escape [literal](#highlight.tags.literal), for example a
  backslash escape in a string.
  */
  escape: t(literal),
  /**
  A color [literal](#highlight.tags.literal).
  */
  color: t(literal),
  /**
  A URL [literal](#highlight.tags.literal).
  */
  url: t(literal),
  /**
  A language keyword.
  */
  keyword,
  /**
  The [keyword](#highlight.tags.keyword) for the self or this
  object.
  */
  self: t(keyword),
  /**
  The [keyword](#highlight.tags.keyword) for null.
  */
  null: t(keyword),
  /**
  A [keyword](#highlight.tags.keyword) denoting some atomic value.
  */
  atom: t(keyword),
  /**
  A [keyword](#highlight.tags.keyword) that represents a unit.
  */
  unit: t(keyword),
  /**
  A modifier [keyword](#highlight.tags.keyword).
  */
  modifier: t(keyword),
  /**
  A [keyword](#highlight.tags.keyword) that acts as an operator.
  */
  operatorKeyword: t(keyword),
  /**
  A control-flow related [keyword](#highlight.tags.keyword).
  */
  controlKeyword: t(keyword),
  /**
  A [keyword](#highlight.tags.keyword) that defines something.
  */
  definitionKeyword: t(keyword),
  /**
  A [keyword](#highlight.tags.keyword) related to defining or
  interfacing with modules.
  */
  moduleKeyword: t(keyword),
  /**
  An operator.
  */
  operator,
  /**
  An [operator](#highlight.tags.operator) that dereferences something.
  */
  derefOperator: t(operator),
  /**
  Arithmetic-related [operator](#highlight.tags.operator).
  */
  arithmeticOperator: t(operator),
  /**
  Logical [operator](#highlight.tags.operator).
  */
  logicOperator: t(operator),
  /**
  Bit [operator](#highlight.tags.operator).
  */
  bitwiseOperator: t(operator),
  /**
  Comparison [operator](#highlight.tags.operator).
  */
  compareOperator: t(operator),
  /**
  [Operator](#highlight.tags.operator) that updates its operand.
  */
  updateOperator: t(operator),
  /**
  [Operator](#highlight.tags.operator) that defines something.
  */
  definitionOperator: t(operator),
  /**
  Type-related [operator](#highlight.tags.operator).
  */
  typeOperator: t(operator),
  /**
  Control-flow [operator](#highlight.tags.operator).
  */
  controlOperator: t(operator),
  /**
  Program or markup punctuation.
  */
  punctuation,
  /**
  [Punctuation](#highlight.tags.punctuation) that separates
  things.
  */
  separator: t(punctuation),
  /**
  Bracket-style [punctuation](#highlight.tags.punctuation).
  */
  bracket,
  /**
  Angle [brackets](#highlight.tags.bracket) (usually `<` and `>`
  tokens).
  */
  angleBracket: t(bracket),
  /**
  Square [brackets](#highlight.tags.bracket) (usually `[` and `]`
  tokens).
  */
  squareBracket: t(bracket),
  /**
  Parentheses (usually `(` and `)` tokens). Subtag of
  [bracket](#highlight.tags.bracket).
  */
  paren: t(bracket),
  /**
  Braces (usually `{` and `}` tokens). Subtag of
  [bracket](#highlight.tags.bracket).
  */
  brace: t(bracket),
  /**
  Content, for example plain text in XML or markup documents.
  */
  content,
  /**
  [Content](#highlight.tags.content) that represents a heading.
  */
  heading,
  /**
  A level 1 [heading](#highlight.tags.heading).
  */
  heading1: t(heading),
  /**
  A level 2 [heading](#highlight.tags.heading).
  */
  heading2: t(heading),
  /**
  A level 3 [heading](#highlight.tags.heading).
  */
  heading3: t(heading),
  /**
  A level 4 [heading](#highlight.tags.heading).
  */
  heading4: t(heading),
  /**
  A level 5 [heading](#highlight.tags.heading).
  */
  heading5: t(heading),
  /**
  A level 6 [heading](#highlight.tags.heading).
  */
  heading6: t(heading),
  /**
  A prose [content](#highlight.tags.content) separator (such as a horizontal rule).
  */
  contentSeparator: t(content),
  /**
  [Content](#highlight.tags.content) that represents a list.
  */
  list: t(content),
  /**
  [Content](#highlight.tags.content) that represents a quote.
  */
  quote: t(content),
  /**
  [Content](#highlight.tags.content) that is emphasized.
  */
  emphasis: t(content),
  /**
  [Content](#highlight.tags.content) that is styled strong.
  */
  strong: t(content),
  /**
  [Content](#highlight.tags.content) that is part of a link.
  */
  link: t(content),
  /**
  [Content](#highlight.tags.content) that is styled as code or
  monospace.
  */
  monospace: t(content),
  /**
  [Content](#highlight.tags.content) that has a strike-through
  style.
  */
  strikethrough: t(content),
  /**
  Inserted text in a change-tracking format.
  */
  inserted: t(),
  /**
  Deleted text.
  */
  deleted: t(),
  /**
  Changed text.
  */
  changed: t(),
  /**
  An invalid or unsyntactic element.
  */
  invalid: t(),
  /**
  Metadata or meta-instruction.
  */
  meta,
  /**
  [Metadata](#highlight.tags.meta) that applies to the entire
  document.
  */
  documentMeta: t(meta),
  /**
  [Metadata](#highlight.tags.meta) that annotates or adds
  attributes to a given syntactic element.
  */
  annotation: t(meta),
  /**
  Processing instruction or preprocessor directive. Subtag of
  [meta](#highlight.tags.meta).
  */
  processingInstruction: t(meta),
  /**
  [Modifier](#highlight.Tag^defineModifier) that indicates that a
  given element is being defined. Expected to be used with the
  various [name](#highlight.tags.name) tags.
  */
  definition: Tag.defineModifier("definition"),
  /**
  [Modifier](#highlight.Tag^defineModifier) that indicates that
  something is constant. Mostly expected to be used with
  [variable names](#highlight.tags.variableName).
  */
  constant: Tag.defineModifier("constant"),
  /**
  [Modifier](#highlight.Tag^defineModifier) used to indicate that
  a [variable](#highlight.tags.variableName) or [property
  name](#highlight.tags.propertyName) is being called or defined
  as a function.
  */
  function: Tag.defineModifier("function"),
  /**
  [Modifier](#highlight.Tag^defineModifier) that can be applied to
  [names](#highlight.tags.name) to indicate that they belong to
  the language's standard environment.
  */
  standard: Tag.defineModifier("standard"),
  /**
  [Modifier](#highlight.Tag^defineModifier) that indicates a given
  [names](#highlight.tags.name) is local to some scope.
  */
  local: Tag.defineModifier("local"),
  /**
  A generic variant [modifier](#highlight.Tag^defineModifier) that
  can be used to tag language-specific alternative variants of
  some common tag. It is recommended for themes to define special
  forms of at least the [string](#highlight.tags.string) and
  [variable name](#highlight.tags.variableName) tags, since those
  come up a lot.
  */
  special: Tag.defineModifier("special")
};
for (let name2 in tags) {
  let val = tags[name2];
  if (val instanceof Tag)
    val.name = name2;
}
var classHighlighter = tagHighlighter([
  { tag: tags.link, class: "tok-link" },
  { tag: tags.heading, class: "tok-heading" },
  { tag: tags.emphasis, class: "tok-emphasis" },
  { tag: tags.strong, class: "tok-strong" },
  { tag: tags.keyword, class: "tok-keyword" },
  { tag: tags.atom, class: "tok-atom" },
  { tag: tags.bool, class: "tok-bool" },
  { tag: tags.url, class: "tok-url" },
  { tag: tags.labelName, class: "tok-labelName" },
  { tag: tags.inserted, class: "tok-inserted" },
  { tag: tags.deleted, class: "tok-deleted" },
  { tag: tags.literal, class: "tok-literal" },
  { tag: tags.string, class: "tok-string" },
  { tag: tags.number, class: "tok-number" },
  { tag: [tags.regexp, tags.escape, tags.special(tags.string)], class: "tok-string2" },
  { tag: tags.variableName, class: "tok-variableName" },
  { tag: tags.local(tags.variableName), class: "tok-variableName tok-local" },
  { tag: tags.definition(tags.variableName), class: "tok-variableName tok-definition" },
  { tag: tags.special(tags.variableName), class: "tok-variableName2" },
  { tag: tags.definition(tags.propertyName), class: "tok-propertyName tok-definition" },
  { tag: tags.typeName, class: "tok-typeName" },
  { tag: tags.namespace, class: "tok-namespace" },
  { tag: tags.className, class: "tok-className" },
  { tag: tags.macroName, class: "tok-macroName" },
  { tag: tags.propertyName, class: "tok-propertyName" },
  { tag: tags.operator, class: "tok-operator" },
  { tag: tags.comment, class: "tok-comment" },
  { tag: tags.meta, class: "tok-meta" },
  { tag: tags.invalid, class: "tok-invalid" },
  { tag: tags.punctuation, class: "tok-punctuation" }
]);

// node_modules/@lezer/python/dist/index.js
var printKeyword = 1;
var indent = 194;
var dedent = 195;
var newline$1 = 196;
var blankLineStart = 197;
var newlineBracketed = 198;
var eof = 199;
var stringContent = 200;
var Escape = 2;
var replacementStart = 3;
var stringEnd = 201;
var ParenL = 24;
var ParenthesizedExpression = 25;
var TupleExpression = 49;
var ComprehensionExpression = 50;
var BracketL = 55;
var ArrayExpression = 56;
var ArrayComprehensionExpression = 57;
var BraceL = 59;
var DictionaryExpression = 60;
var DictionaryComprehensionExpression = 61;
var SetExpression = 62;
var SetComprehensionExpression = 63;
var ArgList = 65;
var subscript = 238;
var String$1 = 71;
var stringStart = 241;
var stringStartD = 242;
var stringStartL = 243;
var stringStartLD = 244;
var stringStartR = 245;
var stringStartRD = 246;
var stringStartRL = 247;
var stringStartRLD = 248;
var FormatString = 72;
var stringStartF = 249;
var stringStartFD = 250;
var stringStartFL = 251;
var stringStartFLD = 252;
var stringStartFR = 253;
var stringStartFRD = 254;
var stringStartFRL = 255;
var stringStartFRLD = 256;
var FormatReplacement = 73;
var nestedFormatReplacement = 77;
var importList = 263;
var TypeParamList = 112;
var ParamList = 130;
var SequencePattern = 151;
var MappingPattern = 152;
var PatternArgList = 155;
var newline = 10;
var carriageReturn = 13;
var space = 32;
var tab = 9;
var hash = 35;
var parenOpen = 40;
var dot = 46;
var braceOpen = 123;
var braceClose = 125;
var singleQuote = 39;
var doubleQuote = 34;
var backslash = 92;
var letter_o = 111;
var letter_x = 120;
var letter_N = 78;
var letter_u = 117;
var letter_U = 85;
var bracketed = /* @__PURE__ */ new Set([
  ParenthesizedExpression,
  TupleExpression,
  ComprehensionExpression,
  importList,
  ArgList,
  ParamList,
  ArrayExpression,
  ArrayComprehensionExpression,
  subscript,
  SetExpression,
  SetComprehensionExpression,
  FormatString,
  FormatReplacement,
  nestedFormatReplacement,
  DictionaryExpression,
  DictionaryComprehensionExpression,
  SequencePattern,
  MappingPattern,
  PatternArgList,
  TypeParamList
]);
function isLineBreak(ch) {
  return ch == newline || ch == carriageReturn;
}
function isHex(ch) {
  return ch >= 48 && ch <= 57 || ch >= 65 && ch <= 70 || ch >= 97 && ch <= 102;
}
var newlines = new ExternalTokenizer((input, stack) => {
  let prev;
  if (input.next < 0) {
    input.acceptToken(eof);
  } else if (stack.context.flags & cx_Bracketed) {
    if (isLineBreak(input.next)) input.acceptToken(newlineBracketed, 1);
  } else if (((prev = input.peek(-1)) < 0 || isLineBreak(prev)) && stack.canShift(blankLineStart)) {
    let spaces = 0;
    while (input.next == space || input.next == tab) {
      input.advance();
      spaces++;
    }
    if (input.next == newline || input.next == carriageReturn || input.next == hash)
      input.acceptToken(blankLineStart, -spaces);
  } else if (isLineBreak(input.next)) {
    input.acceptToken(newline$1, 1);
  }
}, { contextual: true });
var indentation = new ExternalTokenizer((input, stack) => {
  let context = stack.context;
  if (context.flags) return;
  let prev = input.peek(-1);
  if (prev == newline || prev == carriageReturn) {
    let depth = 0, chars = 0;
    for (; ; ) {
      if (input.next == space) depth++;
      else if (input.next == tab) depth += 8 - depth % 8;
      else break;
      input.advance();
      chars++;
    }
    if (depth != context.indent && input.next != newline && input.next != carriageReturn && input.next != hash) {
      if (depth < context.indent) input.acceptToken(dedent, -chars);
      else input.acceptToken(indent);
    }
  }
});
var cx_Bracketed = 1;
var cx_String = 2;
var cx_DoubleQuote = 4;
var cx_Long = 8;
var cx_Raw = 16;
var cx_Format = 32;
function Context(parent, indent2, flags) {
  this.parent = parent;
  this.indent = indent2;
  this.flags = flags;
  this.hash = (parent ? parent.hash + parent.hash << 8 : 0) + indent2 + (indent2 << 4) + flags + (flags << 6);
}
var topIndent = new Context(null, 0, 0);
function countIndent(space2) {
  let depth = 0;
  for (let i = 0; i < space2.length; i++)
    depth += space2.charCodeAt(i) == tab ? 8 - depth % 8 : 1;
  return depth;
}
var stringFlags = new Map([
  [stringStart, 0],
  [stringStartD, cx_DoubleQuote],
  [stringStartL, cx_Long],
  [stringStartLD, cx_Long | cx_DoubleQuote],
  [stringStartR, cx_Raw],
  [stringStartRD, cx_Raw | cx_DoubleQuote],
  [stringStartRL, cx_Raw | cx_Long],
  [stringStartRLD, cx_Raw | cx_Long | cx_DoubleQuote],
  [stringStartF, cx_Format],
  [stringStartFD, cx_Format | cx_DoubleQuote],
  [stringStartFL, cx_Format | cx_Long],
  [stringStartFLD, cx_Format | cx_Long | cx_DoubleQuote],
  [stringStartFR, cx_Format | cx_Raw],
  [stringStartFRD, cx_Format | cx_Raw | cx_DoubleQuote],
  [stringStartFRL, cx_Format | cx_Raw | cx_Long],
  [stringStartFRLD, cx_Format | cx_Raw | cx_Long | cx_DoubleQuote]
].map(([term, flags]) => [term, flags | cx_String]));
var trackIndent = new ContextTracker({
  start: topIndent,
  reduce(context, term, _, input) {
    if (context.flags & cx_Bracketed && bracketed.has(term) || (term == String$1 || term == FormatString) && context.flags & cx_String)
      return context.parent;
    return context;
  },
  shift(context, term, stack, input) {
    if (term == indent)
      return new Context(context, countIndent(input.read(input.pos, stack.pos)), 0);
    if (term == dedent)
      return context.parent;
    if (term == ParenL || term == BracketL || term == BraceL || term == replacementStart)
      return new Context(context, 0, cx_Bracketed);
    if (stringFlags.has(term))
      return new Context(context, 0, stringFlags.get(term) | context.flags & cx_Bracketed);
    return context;
  },
  hash(context) {
    return context.hash;
  }
});
var legacyPrint = new ExternalTokenizer((input) => {
  for (let i = 0; i < 5; i++) {
    if (input.next != "print".charCodeAt(i)) return;
    input.advance();
  }
  if (/\w/.test(String.fromCharCode(input.next))) return;
  for (let off = 0; ; off++) {
    let next = input.peek(off);
    if (next == space || next == tab) continue;
    if (next != parenOpen && next != dot && next != newline && next != carriageReturn && next != hash)
      input.acceptToken(printKeyword);
    return;
  }
});
var strings = new ExternalTokenizer((input, stack) => {
  let { flags } = stack.context;
  let quote = flags & cx_DoubleQuote ? doubleQuote : singleQuote;
  let long = (flags & cx_Long) > 0;
  let escapes = !(flags & cx_Raw);
  let format = (flags & cx_Format) > 0;
  let start = input.pos;
  for (; ; ) {
    if (input.next < 0) {
      break;
    } else if (format && input.next == braceOpen) {
      if (input.peek(1) == braceOpen) {
        input.advance(2);
      } else {
        if (input.pos == start) {
          input.acceptToken(replacementStart, 1);
          return;
        }
        break;
      }
    } else if (escapes && input.next == backslash) {
      if (input.pos == start) {
        input.advance();
        let escaped = input.next;
        if (escaped >= 0) {
          input.advance();
          skipEscape(input, escaped);
        }
        input.acceptToken(Escape);
        return;
      }
      break;
    } else if (input.next == backslash && !escapes && input.peek(1) > -1) {
      input.advance(2);
    } else if (input.next == quote && (!long || input.peek(1) == quote && input.peek(2) == quote)) {
      if (input.pos == start) {
        input.acceptToken(stringEnd, long ? 3 : 1);
        return;
      }
      break;
    } else if (input.next == newline) {
      if (long) {
        input.advance();
      } else if (input.pos == start) {
        input.acceptToken(stringEnd);
        return;
      }
      break;
    } else {
      input.advance();
    }
  }
  if (input.pos > start) input.acceptToken(stringContent);
});
function skipEscape(input, ch) {
  if (ch == letter_o) {
    for (let i = 0; i < 2 && input.next >= 48 && input.next <= 55; i++) input.advance();
  } else if (ch == letter_x) {
    for (let i = 0; i < 2 && isHex(input.next); i++) input.advance();
  } else if (ch == letter_u) {
    for (let i = 0; i < 4 && isHex(input.next); i++) input.advance();
  } else if (ch == letter_U) {
    for (let i = 0; i < 8 && isHex(input.next); i++) input.advance();
  } else if (ch == letter_N) {
    if (input.next == braceOpen) {
      input.advance();
      while (input.next >= 0 && input.next != braceClose && input.next != singleQuote && input.next != doubleQuote && input.next != newline) input.advance();
      if (input.next == braceClose) input.advance();
    }
  }
}
var pythonHighlighting = styleTags({
  'async "*" "**" FormatConversion FormatSpec': tags.modifier,
  "for while if elif else try except finally return raise break continue with pass assert await yield match case": tags.controlKeyword,
  "in not and or is del": tags.operatorKeyword,
  "from def class global nonlocal lambda": tags.definitionKeyword,
  import: tags.moduleKeyword,
  "with as print": tags.keyword,
  Boolean: tags.bool,
  None: tags.null,
  VariableName: tags.variableName,
  "CallExpression/VariableName": tags.function(tags.variableName),
  "FunctionDefinition/VariableName": tags.function(tags.definition(tags.variableName)),
  "ClassDefinition/VariableName": tags.definition(tags.className),
  PropertyName: tags.propertyName,
  "CallExpression/MemberExpression/PropertyName": tags.function(tags.propertyName),
  Comment: tags.lineComment,
  Number: tags.number,
  String: tags.string,
  FormatString: tags.special(tags.string),
  Escape: tags.escape,
  UpdateOp: tags.updateOperator,
  "ArithOp!": tags.arithmeticOperator,
  BitOp: tags.bitwiseOperator,
  CompareOp: tags.compareOperator,
  AssignOp: tags.definitionOperator,
  Ellipsis: tags.punctuation,
  At: tags.meta,
  "( )": tags.paren,
  "[ ]": tags.squareBracket,
  "{ }": tags.brace,
  ".": tags.derefOperator,
  ", ;": tags.separator
});
var spec_identifier = { __proto__: null, await: 44, or: 54, and: 56, in: 60, not: 62, is: 64, if: 70, else: 72, lambda: 76, yield: 94, from: 96, async: 102, for: 104, None: 162, True: 164, False: 164, del: 178, pass: 182, break: 186, continue: 190, return: 194, raise: 202, import: 206, as: 208, global: 212, nonlocal: 214, assert: 218, type: 223, elif: 236, while: 240, try: 246, except: 248, finally: 250, with: 254, def: 258, class: 268, match: 279, case: 285 };
var parser = LRParser.deserialize({
  version: 14,
  states: "##jQ`QeOOP$}OSOOO&WQtO'#HUOOQS'#Co'#CoOOQS'#Cp'#CpO'vQdO'#CnO*UQtO'#HTOOQS'#HU'#HUOOQS'#DU'#DUOOQS'#HT'#HTO*rQdO'#D_O+VQdO'#DfO+gQdO'#DjO+zOWO'#DuO,VOWO'#DvO.[QtO'#GuOOQS'#Gu'#GuO'vQdO'#GtO0ZQtO'#GtOOQS'#Eb'#EbO0rQdO'#EcOOQS'#Gs'#GsO0|QdO'#GrOOQV'#Gr'#GrO1XQdO'#FYOOQS'#G^'#G^O1^QdO'#FXOOQV'#IS'#ISOOQV'#Gq'#GqOOQV'#Fq'#FqQ`QeOOO'vQdO'#CqO1lQdO'#C}O1sQdO'#DRO2RQdO'#HYO2cQtO'#EVO'vQdO'#EWOOQS'#EY'#EYOOQS'#E['#E[OOQS'#E^'#E^O2wQdO'#E`O3_QdO'#EdO3rQdO'#EfO3zQtO'#EfO1XQdO'#EiO0rQdO'#ElO1XQdO'#EnO0rQdO'#EtO0rQdO'#EwO4VQdO'#EyO4^QdO'#FOO4iQdO'#EzO0rQdO'#FOO1XQdO'#FQO1XQdO'#FVO4nQdO'#F[P4uOdO'#GpPOOO)CBd)CBdOOQS'#Ce'#CeOOQS'#Cf'#CfOOQS'#Cg'#CgOOQS'#Ch'#ChOOQS'#Ci'#CiOOQS'#Cj'#CjOOQS'#Cl'#ClO'vQdO,59OO'vQdO,59OO'vQdO,59OO'vQdO,59OO'vQdO,59OO'vQdO,59OO5TQdO'#DoOOQS,5:Y,5:YO5hQdO'#HdOOQS,5:],5:]O5uQ!fO,5:]O5zQtO,59YO1lQdO,59bO1lQdO,59bO1lQdO,59bO8jQdO,59bO8oQdO,59bO8vQdO,59jO8}QdO'#HTO:TQdO'#HSOOQS'#HS'#HSOOQS'#D['#D[O:lQdO,59aO'vQdO,59aO:zQdO,59aOOQS,59y,59yO;PQdO,5:RO'vQdO,5:ROOQS,5:Q,5:QO;_QdO,5:QO;dQdO,5:XO'vQdO,5:XO'vQdO,5:VOOQS,5:U,5:UO;uQdO,5:UO;zQdO,5:WOOOW'#Fy'#FyO<POWO,5:aOOQS,5:a,5:aO<[QdO'#HwOOOW'#Dw'#DwOOOW'#Fz'#FzO<lOWO,5:bOOQS,5:b,5:bOOQS'#F}'#F}O<zQtO,5:iO?lQtO,5=`O@VQ#xO,5=`O@vQtO,5=`OOQS,5:},5:}OA_QeO'#GWOBqQdO,5;^OOQV,5=^,5=^OB|QtO'#IPOCkQdO,5;tOOQS-E:[-E:[OOQV,5;s,5;sO4dQdO'#FQOOQV-E9o-E9oOCsQtO,59]OEzQtO,59iOFeQdO'#HVOFpQdO'#HVO1XQdO'#HVOF{QdO'#DTOGTQdO,59mOGYQdO'#HZO'vQdO'#HZO0rQdO,5=tOOQS,5=t,5=tO0rQdO'#EROOQS'#ES'#ESOGwQdO'#GPOHXQdO,58|OHXQdO,58|O*xQdO,5:oOHgQtO'#H]OOQS,5:r,5:rOOQS,5:z,5:zOHzQdO,5;OOI]QdO'#IOO1XQdO'#H}OOQS,5;Q,5;QOOQS'#GT'#GTOIqQtO,5;QOJPQdO,5;QOJUQdO'#IQOOQS,5;T,5;TOJdQdO'#H|OOQS,5;W,5;WOJuQdO,5;YO4iQdO,5;`O4iQdO,5;cOJ}QtO'#ITO'vQdO'#ITOKXQdO,5;eO4VQdO,5;eO0rQdO,5;jO1XQdO,5;lOK^QeO'#EuOLjQgO,5;fO!!kQdO'#IUO4iQdO,5;jO!!vQdO,5;lO!#OQdO,5;qO!#ZQtO,5;vO'vQdO,5;vPOOO,5=[,5=[P!#bOSO,5=[P!#jOdO,5=[O!&bQtO1G.jO!&iQtO1G.jO!)YQtO1G.jO!)dQtO1G.jO!+}QtO1G.jO!,bQtO1G.jO!,uQdO'#HcO!-TQtO'#GuO0rQdO'#HcO!-_QdO'#HbOOQS,5:Z,5:ZO!-gQdO,5:ZO!-lQdO'#HeO!-wQdO'#HeO!.[QdO,5>OOOQS'#Ds'#DsOOQS1G/w1G/wOOQS1G.|1G.|O!/[QtO1G.|O!/cQtO1G.|O1lQdO1G.|O!0OQdO1G/UOOQS'#DZ'#DZO0rQdO,59tOOQS1G.{1G.{O!0VQdO1G/eO!0gQdO1G/eO!0oQdO1G/fO'vQdO'#H[O!0tQdO'#H[O!0yQtO1G.{O!1ZQdO,59iO!2aQdO,5=zO!2qQdO,5=zO!2yQdO1G/mO!3OQtO1G/mOOQS1G/l1G/lO!3`QdO,5=uO!4VQdO,5=uO0rQdO1G/qO!4tQdO1G/sO!4yQtO1G/sO!5ZQtO1G/qOOQS1G/p1G/pOOQS1G/r1G/rOOOW-E9w-E9wOOQS1G/{1G/{O!5kQdO'#HxO0rQdO'#HxO!5|QdO,5>cOOOW-E9x-E9xOOQS1G/|1G/|OOQS-E9{-E9{O!6[Q#xO1G2zO!6{QtO1G2zO'vQdO,5<jOOQS,5<j,5<jOOQS-E9|-E9|OOQS,5<r,5<rOOQS-E:U-E:UOOQV1G0x1G0xO1XQdO'#GRO!7dQtO,5>kOOQS1G1`1G1`O!8RQdO1G1`OOQS'#DV'#DVO0rQdO,5=qOOQS,5=q,5=qO!8WQdO'#FrO!8cQdO,59oO!8kQdO1G/XO!8uQtO,5=uOOQS1G3`1G3`OOQS,5:m,5:mO!9fQdO'#GtOOQS,5<k,5<kOOQS-E9}-E9}O!9wQdO1G.hOOQS1G0Z1G0ZO!:VQdO,5=wO!:gQdO,5=wO0rQdO1G0jO0rQdO1G0jO!:xQdO,5>jO!;ZQdO,5>jO1XQdO,5>jO!;lQdO,5>iOOQS-E:R-E:RO!;qQdO1G0lO!;|QdO1G0lO!<RQdO,5>lO!<aQdO,5>lO!<oQdO,5>hO!=VQdO,5>hO!=hQdO'#EpO0rQdO1G0tO!=sQdO1G0tO!=xQgO1G0zO!AvQgO1G0}O!EqQdO,5>oO!E{QdO,5>oO!FTQtO,5>oO0rQdO1G1PO!F_QdO1G1PO4iQdO1G1UO!!vQdO1G1WOOQV,5;a,5;aO!FdQfO,5;aO!FiQgO1G1QO!JjQdO'#GZO4iQdO1G1QO4iQdO1G1QO!JzQdO,5>pO!KXQdO,5>pO1XQdO,5>pOOQV1G1U1G1UO!KaQdO'#FSO!KrQ!fO1G1WO!KzQdO1G1WOOQV1G1]1G1]O4iQdO1G1]O!LPQdO1G1]O!LXQdO'#F^OOQV1G1b1G1bO!#ZQtO1G1bPOOO1G2v1G2vP!L^OSO1G2vOOQS,5=},5=}OOQS'#Dp'#DpO0rQdO,5=}O!LfQdO,5=|O!LyQdO,5=|OOQS1G/u1G/uO!MRQdO,5>PO!McQdO,5>PO!MkQdO,5>PO!NOQdO,5>PO!N`QdO,5>POOQS1G3j1G3jOOQS7+$h7+$hO!8kQdO7+$pO#!RQdO1G.|O#!YQdO1G.|OOQS1G/`1G/`OOQS,5<`,5<`O'vQdO,5<`OOQS7+%P7+%PO#!aQdO7+%POOQS-E9r-E9rOOQS7+%Q7+%QO#!qQdO,5=vO'vQdO,5=vOOQS7+$g7+$gO#!vQdO7+%PO##OQdO7+%QO##TQdO1G3fOOQS7+%X7+%XO##eQdO1G3fO##mQdO7+%XOOQS,5<_,5<_O'vQdO,5<_O##rQdO1G3aOOQS-E9q-E9qO#$iQdO7+%]OOQS7+%_7+%_O#$wQdO1G3aO#%fQdO7+%_O#%kQdO1G3gO#%{QdO1G3gO#&TQdO7+%]O#&YQdO,5>dO#&sQdO,5>dO#&sQdO,5>dOOQS'#Dx'#DxO#'UO&jO'#DzO#'aO`O'#HyOOOW1G3}1G3}O#'fQdO1G3}O#'nQdO1G3}O#'yQ#xO7+(fO#(jQtO1G2UP#)TQdO'#GOOOQS,5<m,5<mOOQS-E:P-E:POOQS7+&z7+&zOOQS1G3]1G3]OOQS,5<^,5<^OOQS-E9p-E9pOOQS7+$s7+$sO#)bQdO,5=`O#){QdO,5=`O#*^QtO,5<aO#*qQdO1G3cOOQS-E9s-E9sOOQS7+&U7+&UO#+RQdO7+&UO#+aQdO,5<nO#+uQdO1G4UOOQS-E:Q-E:QO#,WQdO1G4UOOQS1G4T1G4TOOQS7+&W7+&WO#,iQdO7+&WOOQS,5<p,5<pO#,tQdO1G4WOOQS-E:S-E:SOOQS,5<l,5<lO#-SQdO1G4SOOQS-E:O-E:OO1XQdO'#EqO#-jQdO'#EqO#-uQdO'#IRO#-}QdO,5;[OOQS7+&`7+&`O0rQdO7+&`O#.SQgO7+&fO!JmQdO'#GXO4iQdO7+&fO4iQdO7+&iO#2QQtO,5<tO'vQdO,5<tO#2[QdO1G4ZOOQS-E:W-E:WO#2fQdO1G4ZO4iQdO7+&kO0rQdO7+&kOOQV7+&p7+&pO!KrQ!fO7+&rO!KzQdO7+&rO`QeO1G0{OOQV-E:X-E:XO4iQdO7+&lO4iQdO7+&lOOQV,5<u,5<uO#2nQdO,5<uO!JmQdO,5<uOOQV7+&l7+&lO#2yQgO7+&lO#6tQdO,5<vO#7PQdO1G4[OOQS-E:Y-E:YO#7^QdO1G4[O#7fQdO'#IWO#7tQdO'#IWO1XQdO'#IWOOQS'#IW'#IWO#8PQdO'#IVOOQS,5;n,5;nO#8XQdO,5;nO0rQdO'#FUOOQV7+&r7+&rO4iQdO7+&rOOQV7+&w7+&wO4iQdO7+&wO#8^QfO,5;xOOQV7+&|7+&|POOO7+(b7+(bO#8cQdO1G3iOOQS,5<c,5<cO#8qQdO1G3hOOQS-E9u-E9uO#9UQdO,5<dO#9aQdO,5<dO#9tQdO1G3kOOQS-E9v-E9vO#:UQdO1G3kO#:^QdO1G3kO#:nQdO1G3kO#:UQdO1G3kOOQS<<H[<<H[O#:yQtO1G1zOOQS<<Hk<<HkP#;WQdO'#FtO8vQdO1G3bO#;eQdO1G3bO#;jQdO<<HkOOQS<<Hl<<HlO#;zQdO7+)QOOQS<<Hs<<HsO#<[QtO1G1yP#<{QdO'#FsO#=YQdO7+)RO#=jQdO7+)RO#=rQdO<<HwO#=wQdO7+({OOQS<<Hy<<HyO#>nQdO,5<bO'vQdO,5<bOOQS-E9t-E9tOOQS<<Hw<<HwOOQS,5<g,5<gO0rQdO,5<gO#>sQdO1G4OOOQS-E9y-E9yO#?^QdO1G4OO<[QdO'#H{OOOO'#D{'#D{OOOO'#F|'#F|O#?oO&jO,5:fOOOW,5>e,5>eOOOW7+)i7+)iO#?zQdO7+)iO#@SQdO1G2zO#@mQdO1G2zP'vQdO'#FuO0rQdO<<IpO1XQdO1G2YP1XQdO'#GSO#AOQdO7+)pO#AaQdO7+)pOOQS<<Ir<<IrP1XQdO'#GUP0rQdO'#GQOOQS,5;],5;]O#ArQdO,5>mO#BQQdO,5>mOOQS1G0v1G0vOOQS<<Iz<<IzOOQV-E:V-E:VO4iQdO<<JQOOQV,5<s,5<sO4iQdO,5<sOOQV<<JQ<<JQOOQV<<JT<<JTO#BYQtO1G2`P#BdQdO'#GYO#BkQdO7+)uO#BuQgO<<JVO4iQdO<<JVOOQV<<J^<<J^O4iQdO<<J^O!KrQ!fO<<J^O#FpQgO7+&gOOQV<<JW<<JWO#FzQgO<<JWOOQV1G2a1G2aO1XQdO1G2aO#JuQdO1G2aO4iQdO<<JWO1XQdO1G2bP0rQdO'#G[O#KQQdO7+)vO#K_QdO7+)vOOQS'#FT'#FTO0rQdO,5>rO#KgQdO,5>rO#KrQdO,5>rO#K}QdO,5>qO#L`QdO,5>qOOQS1G1Y1G1YOOQS,5;p,5;pOOQV<<Jc<<JcO#LhQdO1G1dOOQS7+)T7+)TP#LmQdO'#FwO#L}QdO1G2OO#MbQdO1G2OO#MrQdO1G2OP#M}QdO'#FxO#N[QdO7+)VO#NlQdO7+)VO#NlQdO7+)VO#NtQdO7+)VO$ UQdO7+(|O8vQdO7+(|OOQSAN>VAN>VO$ oQdO<<LmOOQSAN>cAN>cO0rQdO1G1|O$!PQtO1G1|P$!ZQdO'#FvOOQS1G2R1G2RP$!hQdO'#F{O$!uQdO7+)jO$#`QdO,5>gOOOO-E9z-E9zOOOW<<MT<<MTO$#nQdO7+(fOOQSAN?[AN?[OOQS7+'t7+'tO$$XQdO<<M[OOQS,5<q,5<qO$$jQdO1G4XOOQS-E:T-E:TOOQVAN?lAN?lOOQV1G2_1G2_O4iQdOAN?qO$$xQgOAN?qOOQVAN?xAN?xO4iQdOAN?xOOQV<<JR<<JRO4iQdOAN?rO4iQdO7+'{OOQV7+'{7+'{O1XQdO7+'{OOQVAN?rAN?rOOQS7+'|7+'|O$(sQdO<<MbOOQS1G4^1G4^O0rQdO1G4^OOQS,5<w,5<wO$)QQdO1G4]OOQS-E:Z-E:ZOOQU'#G_'#G_O$)cQfO7+'OO$)nQdO'#F_O$*uQdO7+'jO$+VQdO7+'jOOQS7+'j7+'jO$+bQdO<<LqO$+rQdO<<LqO$+rQdO<<LqO$+zQdO'#H^OOQS<<Lh<<LhO$,UQdO<<LhOOQS7+'h7+'hOOQS'#D|'#D|OOOO1G4R1G4RO$,oQdO1G4RO$,wQdO1G4RP!=hQdO'#GVOOQVG25]G25]O4iQdOG25]OOQVG25dG25dOOQVG25^G25^OOQV<<Kg<<KgO4iQdO<<KgOOQS7+)x7+)xP$-SQdO'#G]OOQU-E:]-E:]OOQV<<Jj<<JjO$-vQtO'#FaOOQS'#Fc'#FcO$.WQdO'#FbO$.xQdO'#FbOOQS'#Fb'#FbO$.}QdO'#IYO$)nQdO'#FiO$)nQdO'#FiO$/fQdO'#FjO$)nQdO'#FkO$/mQdO'#IZOOQS'#IZ'#IZO$0[QdO,5;yOOQS<<KU<<KUO$0dQdO<<KUO$0tQdOANB]O$1UQdOANB]O$1^QdO'#H_OOQS'#H_'#H_O1sQdO'#DcO$1wQdO,5=xOOQSANBSANBSOOOO7+)m7+)mO$2`QdO7+)mOOQVLD*wLD*wOOQVANARANARO5uQ!fO'#GaO$2hQtO,5<SO$)nQdO'#FmOOQS,5<W,5<WOOQS'#Fd'#FdO$3YQdO,5;|O$3_QdO,5;|OOQS'#Fg'#FgO$)nQdO'#G`O$4PQdO,5<QO$4kQdO,5>tO$4{QdO,5>tO1XQdO,5<PO$5^QdO,5<TO$5cQdO,5<TO$)nQdO'#I[O$5hQdO'#I[O$5mQdO,5<UOOQS,5<V,5<VO0rQdO'#FpOOQU1G1e1G1eO4iQdO1G1eOOQSAN@pAN@pO$5rQdOG27wO$6SQdO,59}OOQS1G3d1G3dOOOO<<MX<<MXOOQS,5<{,5<{OOQS-E:_-E:_O$6XQtO'#FaO$6`QdO'#I]O$6nQdO'#I]O$6vQdO,5<XOOQS1G1h1G1hO$6{QdO1G1hO$7QQdO,5<zOOQS-E:^-E:^O$7lQdO,5=OO$8TQdO1G4`OOQS-E:b-E:bOOQS1G1k1G1kOOQS1G1o1G1oO$8eQdO,5>vO$)nQdO,5>vOOQS1G1p1G1pOOQS,5<[,5<[OOQU7+'P7+'PO$+zQdO1G/iO$)nQdO,5<YO$8sQdO,5>wO$8zQdO,5>wOOQS1G1s1G1sOOQS7+'S7+'SP$)nQdO'#GdO$9SQdO1G4bO$9^QdO1G4bO$9fQdO1G4bOOQS7+%T7+%TO$9tQdO1G1tO$:SQtO'#FaO$:ZQdO,5<}OOQS,5<},5<}O$:iQdO1G4cOOQS-E:a-E:aO$)nQdO,5<|O$:pQdO,5<|O$:uQdO7+)|OOQS-E:`-E:`O$;PQdO7+)|O$)nQdO,5<ZP$)nQdO'#GcO$;XQdO1G2hO$)nQdO1G2hP$;gQdO'#GbO$;nQdO<<MhO$;xQdO1G1uO$<WQdO7+(SO8vQdO'#C}O8vQdO,59bO8vQdO,59bO8vQdO,59bO$<fQtO,5=`O8vQdO1G.|O0rQdO1G/XO0rQdO7+$pP$<yQdO'#GOO'vQdO'#GtO$=WQdO,59bO$=]QdO,59bO$=dQdO,59mO$=iQdO1G/UO1sQdO'#DRO8vQdO,59j",
  stateData: "$>S~O%cOS%^OSSOS%]PQ~OPdOVaOfoOhYOopOs!POvqO!PrO!Q{O!T!SO!U!RO!XZO!][O!h`O!r`O!s`O!t`O!{tO!}uO#PvO#RwO#TxO#XyO#ZzO#^|O#_|O#a}O#c!OO#l!QO#o!TO#s!UO#u!VO#z!WO#}hO$P!XO%oRO%pRO%tSO%uWO&Z]O&[]O&]]O&^]O&_]O&`]O&a]O&b]O&c^O&d^O&e^O&f^O&g^O&h^O&i^O&j^O~O%]!YO~OV!aO_!aOa!bOh!iO!X!kO!f!mO%j![O%k!]O%l!^O%m!_O%n!_O%o!`O%p!`O%q!aO%r!aO%s!aO~Ok%xXl%xXm%xXn%xXo%xXp%xXs%xXz%xX{%xX!x%xX#g%xX%[%xX%_%xX%z%xXg%xX!T%xX!U%xX%{%xX!W%xX![%xX!Q%xX#[%xXt%xX!m%xX~P%SOfoOhYO!XZO!][O!h`O!r`O!s`O!t`O%oRO%pRO%tSO%uWO&Z]O&[]O&]]O&^]O&_]O&`]O&a]O&b]O&c^O&d^O&e^O&f^O&g^O&h^O&i^O&j^O~Oz%wX{%wX#g%wX%[%wX%_%wX%z%wX~Ok!pOl!qOm!oOn!oOo!rOp!sOs!tO!x%wX~P)pOV!zOg!|Oo0cOv0qO!PrO~P'vOV#OOo0cOv0qO!W#PO~P'vOV#SOa#TOo0cOv0qO![#UO~P'vOQ#XO%`#XO%a#ZO~OQ#^OR#[O%`#^O%a#`O~OV%iX_%iXa%iXh%iXk%iXl%iXm%iXn%iXo%iXp%iXs%iXz%iX!X%iX!f%iX%j%iX%k%iX%l%iX%m%iX%n%iX%o%iX%p%iX%q%iX%r%iX%s%iXg%iX!T%iX!U%iX~O&Z]O&[]O&]]O&^]O&_]O&`]O&a]O&b]O&c^O&d^O&e^O&f^O&g^O&h^O&i^O&j^O{%iX!x%iX#g%iX%[%iX%_%iX%z%iX%{%iX!W%iX![%iX!Q%iX#[%iXt%iX!m%iX~P,eOz#dO{%hX!x%hX#g%hX%[%hX%_%hX%z%hX~Oo0cOv0qO~P'vO#g#gO%[#iO%_#iO~O%uWO~O!T#nO#u!VO#z!WO#}hO~OopO~P'vOV#sOa#tO%uWO{wP~OV#xOo0cOv0qO!Q#yO~P'vO{#{O!x$QO%z#|O#g!yX%[!yX%_!yX~OV#xOo0cOv0qO#g#SX%[#SX%_#SX~P'vOo0cOv0qO#g#WX%[#WX%_#WX~P'vOh$WO%uWO~O!f$YO!r$YO%uWO~OV$eO~P'vO!U$gO#s$hO#u$iO~O{$jO~OV$qO~P'vOS$sO%[$rO%_$rO%c$tO~OV$}Oa$}Og%POo0cOv0qO~P'vOo0cOv0qO{%SO~P'vO&Y%UO~Oa!bOh!iO!X!kO!f!mOVba_bakbalbambanbaobapbasbazba{ba!xba#gba%[ba%_ba%jba%kba%lba%mba%nba%oba%pba%qba%rba%sba%zbagba!Tba!Uba%{ba!Wba![ba!Qba#[batba!mba~On%ZO~Oo%ZO~P'vOo0cO~P'vOk0eOl0fOm0dOn0dOo0mOp0nOs0rOg%wX!T%wX!U%wX%{%wX!W%wX![%wX!Q%wX#[%wX!m%wX~P)pO%{%]Og%vXz%vX!T%vX!U%vX!W%vX{%vX~Og%_Oz%`O!T%dO!U%cO~Og%_O~Oz%gO!T%dO!U%cO!W&SX~O!W%kO~Oz%lO{%nO!T%dO!U%cO![%}X~O![%rO~O![%sO~OQ#XO%`#XO%a%uO~OV%wOo0cOv0qO!PrO~P'vOQ#^OR#[O%`#^O%a%zO~OV!qa_!qaa!qah!qak!qal!qam!qan!qao!qap!qas!qaz!qa{!qa!X!qa!f!qa!x!qa#g!qa%[!qa%_!qa%j!qa%k!qa%l!qa%m!qa%n!qa%o!qa%p!qa%q!qa%r!qa%s!qa%z!qag!qa!T!qa!U!qa%{!qa!W!qa![!qa!Q!qa#[!qat!qa!m!qa~P#yOz%|O{%ha!x%ha#g%ha%[%ha%_%ha%z%ha~P%SOV&OOopOvqO{%ha!x%ha#g%ha%[%ha%_%ha%z%ha~P'vOz%|O{%ha!x%ha#g%ha%[%ha%_%ha%z%ha~OPdOVaOopOvqO!PrO!Q{O!{tO!}uO#PvO#RwO#TxO#XyO#ZzO#^|O#_|O#a}O#c!OO#g$zX%[$zX%_$zX~P'vO#g#gO%[&TO%_&TO~O!f&UOh&sX%[&sXz&sX#[&sX#g&sX%_&sX#Z&sXg&sX~Oh!iO%[&WO~Okealeameaneaoeapeaseazea{ea!xea#gea%[ea%_ea%zeagea!Tea!Uea%{ea!Wea![ea!Qea#[eatea!mea~P%SOsqazqa{qa#gqa%[qa%_qa%zqa~Ok!pOl!qOm!oOn!oOo!rOp!sO!xqa~PEcO%z&YOz%yX{%yX~O%uWOz%yX{%yX~Oz&]O{wX~O{&_O~Oz%lO#g%}X%[%}X%_%}Xg%}X{%}X![%}X!m%}X%z%}X~OV0lOo0cOv0qO!PrO~P'vO%z#|O#gUa%[Ua%_Ua~Oz&hO#g&PX%[&PX%_&PXn&PX~P%SOz&kO!Q&jO#g#Wa%[#Wa%_#Wa~Oz&lO#[&nO#g&rX%[&rX%_&rXg&rX~O!f$YO!r$YO#Z&qO%uWO~O#Z&qO~Oz&sO#g&tX%[&tX%_&tX~Oz&uO#g&pX%[&pX%_&pX{&pX~O!X&wO%z&xO~Oz&|On&wX~P%SOn'PO~OPdOVaOopOvqO!PrO!Q{O!{tO!}uO#PvO#RwO#TxO#XyO#ZzO#^|O#_|O#a}O#c!OO%['UO~P'vOt'YO#p'WO#q'XOP#naV#naf#nah#nao#nas#nav#na!P#na!Q#na!T#na!U#na!X#na!]#na!h#na!r#na!s#na!t#na!{#na!}#na#P#na#R#na#T#na#X#na#Z#na#^#na#_#na#a#na#c#na#l#na#o#na#s#na#u#na#z#na#}#na$P#na%X#na%o#na%p#na%t#na%u#na&Z#na&[#na&]#na&^#na&_#na&`#na&a#na&b#na&c#na&d#na&e#na&f#na&g#na&h#na&i#na&j#na%Z#na%_#na~Oz'ZO#[']O{&xX~Oh'_O!X&wO~Oh!iO{$jO!X&wO~O{'eO~P%SO%['hO%_'hO~OS'iO%['hO%_'hO~OV!aO_!aOa!bOh!iO!X!kO!f!mO%l!^O%m!_O%n!_O%o!`O%p!`O%q!aO%r!aO%s!aOkWilWimWinWioWipWisWizWi{Wi!xWi#gWi%[Wi%_Wi%jWi%zWigWi!TWi!UWi%{Wi!WWi![Wi!QWi#[WitWi!mWi~O%k!]O~P!#uO%kWi~P!#uOV!aO_!aOa!bOh!iO!X!kO!f!mO%o!`O%p!`O%q!aO%r!aO%s!aOkWilWimWinWioWipWisWizWi{Wi!xWi#gWi%[Wi%_Wi%jWi%kWi%lWi%zWigWi!TWi!UWi%{Wi!WWi![Wi!QWi#[WitWi!mWi~O%m!_O%n!_O~P!&pO%mWi%nWi~P!&pOa!bOh!iO!X!kO!f!mOkWilWimWinWioWipWisWizWi{Wi!xWi#gWi%[Wi%_Wi%jWi%kWi%lWi%mWi%nWi%oWi%pWi%zWigWi!TWi!UWi%{Wi!WWi![Wi!QWi#[WitWi!mWi~OV!aO_!aO%q!aO%r!aO%s!aO~P!)nOVWi_Wi%qWi%rWi%sWi~P!)nO!T%dO!U%cOg&VXz&VX~O%z'kO%{'kO~P,eOz'mOg&UX~Og'oO~Oz'pO{'rO!W&XX~Oo0cOv0qOz'pO{'sO!W&XX~P'vO!W'uO~Om!oOn!oOo!rOp!sOkjisjizji{ji!xji#gji%[ji%_ji%zji~Ol!qO~P!.aOlji~P!.aOk0eOl0fOm0dOn0dOo0mOp0nO~Ot'wO~P!/jOV'|Og'}Oo0cOv0qO~P'vOg'}Oz(OO~Og(QO~O!U(SO~Og(TOz(OO!T%dO!U%cO~P%SOk0eOl0fOm0dOn0dOo0mOp0nOgqa!Tqa!Uqa%{qa!Wqa![qa!Qqa#[qatqa!mqa~PEcOV'|Oo0cOv0qO!W&Sa~P'vOz(WO!W&Sa~O!W(XO~Oz(WO!T%dO!U%cO!W&Sa~P%SOV(]Oo0cOv0qO![%}a#g%}a%[%}a%_%}ag%}a{%}a!m%}a%z%}a~P'vOz(^O![%}a#g%}a%[%}a%_%}ag%}a{%}a!m%}a%z%}a~O![(aO~Oz(^O!T%dO!U%cO![%}a~P%SOz(dO!T%dO!U%cO![&Ta~P%SOz(gO{&lX![&lX!m&lX%z&lX~O{(kO![(mO!m(nO%z(jO~OV&OOopOvqO{%hi!x%hi#g%hi%[%hi%_%hi%z%hi~P'vOz(pO{%hi!x%hi#g%hi%[%hi%_%hi%z%hi~O!f&UOh&sa%[&saz&sa#[&sa#g&sa%_&sa#Z&sag&sa~O%[(uO~OV#sOa#tO%uWO~Oz&]O{wa~OopOvqO~P'vOz(^O#g%}a%[%}a%_%}ag%}a{%}a![%}a!m%}a%z%}a~P%SOz(zO#g%hX%[%hX%_%hX%z%hX~O%z#|O#gUi%[Ui%_Ui~O#g&Pa%[&Pa%_&Pan&Pa~P'vOz(}O#g&Pa%[&Pa%_&Pan&Pa~O%uWO#g&ra%[&ra%_&rag&ra~Oz)SO#g&ra%[&ra%_&rag&ra~Og)VO~OV)WOh$WO%uWO~O#Z)XO~O%uWO#g&ta%[&ta%_&ta~Oz)ZO#g&ta%[&ta%_&ta~Oo0cOv0qO#g&pa%[&pa%_&pa{&pa~P'vOz)^O#g&pa%[&pa%_&pa{&pa~OV)`Oa)`O%uWO~O%z)eO~Ot)hO#j)gOP#hiV#hif#hih#hio#his#hiv#hi!P#hi!Q#hi!T#hi!U#hi!X#hi!]#hi!h#hi!r#hi!s#hi!t#hi!{#hi!}#hi#P#hi#R#hi#T#hi#X#hi#Z#hi#^#hi#_#hi#a#hi#c#hi#l#hi#o#hi#s#hi#u#hi#z#hi#}#hi$P#hi%X#hi%o#hi%p#hi%t#hi%u#hi&Z#hi&[#hi&]#hi&^#hi&_#hi&`#hi&a#hi&b#hi&c#hi&d#hi&e#hi&f#hi&g#hi&h#hi&i#hi&j#hi%Z#hi%_#hi~Ot)iOP#kiV#kif#kih#kio#kis#kiv#ki!P#ki!Q#ki!T#ki!U#ki!X#ki!]#ki!h#ki!r#ki!s#ki!t#ki!{#ki!}#ki#P#ki#R#ki#T#ki#X#ki#Z#ki#^#ki#_#ki#a#ki#c#ki#l#ki#o#ki#s#ki#u#ki#z#ki#}#ki$P#ki%X#ki%o#ki%p#ki%t#ki%u#ki&Z#ki&[#ki&]#ki&^#ki&_#ki&`#ki&a#ki&b#ki&c#ki&d#ki&e#ki&f#ki&g#ki&h#ki&i#ki&j#ki%Z#ki%_#ki~OV)kOn&wa~P'vOz)lOn&wa~Oz)lOn&wa~P%SOn)pO~O%Y)tO~Ot)wO#p'WO#q)vOP#niV#nif#nih#nio#nis#niv#ni!P#ni!Q#ni!T#ni!U#ni!X#ni!]#ni!h#ni!r#ni!s#ni!t#ni!{#ni!}#ni#P#ni#R#ni#T#ni#X#ni#Z#ni#^#ni#_#ni#a#ni#c#ni#l#ni#o#ni#s#ni#u#ni#z#ni#}#ni$P#ni%X#ni%o#ni%p#ni%t#ni%u#ni&Z#ni&[#ni&]#ni&^#ni&_#ni&`#ni&a#ni&b#ni&c#ni&d#ni&e#ni&f#ni&g#ni&h#ni&i#ni&j#ni%Z#ni%_#ni~OV)zOo0cOv0qO{$jO~P'vOo0cOv0qO{&xa~P'vOz*OO{&xa~OV*SOa*TOg*WO%q*UO%uWO~O{$jO&{*YO~Oh'_O~Oh!iO{$jO~O%[*_O~O%[*aO%_*aO~OV$}Oa$}Oo0cOv0qOg&Ua~P'vOz*dOg&Ua~Oo0cOv0qO{*gO!W&Xa~P'vOz*hO!W&Xa~Oo0cOv0qOz*hO{*kO!W&Xa~P'vOo0cOv0qOz*hO!W&Xa~P'vOz*hO{*kO!W&Xa~Om0dOn0dOo0mOp0nOgjikjisjizji!Tji!Uji%{ji!Wji{ji![ji#gji%[ji%_ji!Qji#[jitji!mji%zji~Ol0fO~P!NkOlji~P!NkOV'|Og*pOo0cOv0qO~P'vOn*rO~Og*pOz*tO~Og*uO~OV'|Oo0cOv0qO!W&Si~P'vOz*vO!W&Si~O!W*wO~OV(]Oo0cOv0qO![%}i#g%}i%[%}i%_%}ig%}i{%}i!m%}i%z%}i~P'vOz*zO!T%dO!U%cO![&Ti~Oz*}O![%}i#g%}i%[%}i%_%}ig%}i{%}i!m%}i%z%}i~O![+OO~Oa+QOo0cOv0qO![&Ti~P'vOz*zO![&Ti~O![+SO~OV+UOo0cOv0qO{&la![&la!m&la%z&la~P'vOz+VO{&la![&la!m&la%z&la~O!]+YO&n+[O![!nX~O![+^O~O{(kO![+_O~O{(kO![+_O!m+`O~OV&OOopOvqO{%hq!x%hq#g%hq%[%hq%_%hq%z%hq~P'vOz$ri{$ri!x$ri#g$ri%[$ri%_$ri%z$ri~P%SOV&OOopOvqO~P'vOV&OOo0cOv0qO#g%ha%[%ha%_%ha%z%ha~P'vOz+aO#g%ha%[%ha%_%ha%z%ha~Oz$ia#g$ia%[$ia%_$ian$ia~P%SO#g&Pi%[&Pi%_&Pin&Pi~P'vOz+dO#g#Wq%[#Wq%_#Wq~O#[+eOz$va#g$va%[$va%_$vag$va~O%uWO#g&ri%[&ri%_&rig&ri~Oz+gO#g&ri%[&ri%_&rig&ri~OV+iOh$WO%uWO~O%uWO#g&ti%[&ti%_&ti~Oo0cOv0qO#g&pi%[&pi%_&pi{&pi~P'vO{#{Oz#eX!W#eX~Oz+mO!W&uX~O!W+oO~Ot+rO#j)gOP#hqV#hqf#hqh#hqo#hqs#hqv#hq!P#hq!Q#hq!T#hq!U#hq!X#hq!]#hq!h#hq!r#hq!s#hq!t#hq!{#hq!}#hq#P#hq#R#hq#T#hq#X#hq#Z#hq#^#hq#_#hq#a#hq#c#hq#l#hq#o#hq#s#hq#u#hq#z#hq#}#hq$P#hq%X#hq%o#hq%p#hq%t#hq%u#hq&Z#hq&[#hq&]#hq&^#hq&_#hq&`#hq&a#hq&b#hq&c#hq&d#hq&e#hq&f#hq&g#hq&h#hq&i#hq&j#hq%Z#hq%_#hq~On$|az$|a~P%SOV)kOn&wi~P'vOz+yOn&wi~Oz,TO{$jO#[,TO~O#q,VOP#nqV#nqf#nqh#nqo#nqs#nqv#nq!P#nq!Q#nq!T#nq!U#nq!X#nq!]#nq!h#nq!r#nq!s#nq!t#nq!{#nq!}#nq#P#nq#R#nq#T#nq#X#nq#Z#nq#^#nq#_#nq#a#nq#c#nq#l#nq#o#nq#s#nq#u#nq#z#nq#}#nq$P#nq%X#nq%o#nq%p#nq%t#nq%u#nq&Z#nq&[#nq&]#nq&^#nq&_#nq&`#nq&a#nq&b#nq&c#nq&d#nq&e#nq&f#nq&g#nq&h#nq&i#nq&j#nq%Z#nq%_#nq~O#[,WOz%Oa{%Oa~Oo0cOv0qO{&xi~P'vOz,YO{&xi~O{#{O%z,[Og&zXz&zX~O%uWOg&zXz&zX~Oz,`Og&yX~Og,bO~O%Y,eO~O!T%dO!U%cOg&Viz&Vi~OV$}Oa$}Oo0cOv0qOg&Ui~P'vO{,hOz$la!W$la~Oo0cOv0qO{,iOz$la!W$la~P'vOo0cOv0qO{*gO!W&Xi~P'vOz,lO!W&Xi~Oo0cOv0qOz,lO!W&Xi~P'vOz,lO{,oO!W&Xi~Og$hiz$hi!W$hi~P%SOV'|Oo0cOv0qO~P'vOn,qO~OV'|Og,rOo0cOv0qO~P'vOV'|Oo0cOv0qO!W&Sq~P'vOz$gi![$gi#g$gi%[$gi%_$gig$gi{$gi!m$gi%z$gi~P%SOV(]Oo0cOv0qO~P'vOa+QOo0cOv0qO![&Tq~P'vOz,sO![&Tq~O![,tO~OV(]Oo0cOv0qO![%}q#g%}q%[%}q%_%}qg%}q{%}q!m%}q%z%}q~P'vO{,uO~OV+UOo0cOv0qO{&li![&li!m&li%z&li~P'vOz,zO{&li![&li!m&li%z&li~O!]+YO&n+[O![!na~O{(kO![,}O~OV&OOo0cOv0qO#g%hi%[%hi%_%hi%z%hi~P'vOz-OO#g%hi%[%hi%_%hi%z%hi~O%uWO#g&rq%[&rq%_&rqg&rq~Oz-RO#g&rq%[&rq%_&rqg&rq~OV)`Oa)`O%uWO!W&ua~Oz-TO!W&ua~On$|iz$|i~P%SOV)kO~P'vOV)kOn&wq~P'vOt-XOP#myV#myf#myh#myo#mys#myv#my!P#my!Q#my!T#my!U#my!X#my!]#my!h#my!r#my!s#my!t#my!{#my!}#my#P#my#R#my#T#my#X#my#Z#my#^#my#_#my#a#my#c#my#l#my#o#my#s#my#u#my#z#my#}#my$P#my%X#my%o#my%p#my%t#my%u#my&Z#my&[#my&]#my&^#my&_#my&`#my&a#my&b#my&c#my&d#my&e#my&f#my&g#my&h#my&i#my&j#my%Z#my%_#my~O%Z-]O%_-]O~P`O#q-^OP#nyV#nyf#nyh#nyo#nys#nyv#ny!P#ny!Q#ny!T#ny!U#ny!X#ny!]#ny!h#ny!r#ny!s#ny!t#ny!{#ny!}#ny#P#ny#R#ny#T#ny#X#ny#Z#ny#^#ny#_#ny#a#ny#c#ny#l#ny#o#ny#s#ny#u#ny#z#ny#}#ny$P#ny%X#ny%o#ny%p#ny%t#ny%u#ny&Z#ny&[#ny&]#ny&^#ny&_#ny&`#ny&a#ny&b#ny&c#ny&d#ny&e#ny&f#ny&g#ny&h#ny&i#ny&j#ny%Z#ny%_#ny~Oz-aO{$jO#[-aO~Oo0cOv0qO{&xq~P'vOz-dO{&xq~O%z,[Og&zaz&za~O{#{Og&zaz&za~OV*SOa*TO%q*UO%uWOg&ya~Oz-hOg&ya~O$S-lO~OV$}Oa$}Oo0cOv0qO~P'vOo0cOv0qO{-mOz$li!W$li~P'vOo0cOv0qOz$li!W$li~P'vO{-mOz$li!W$li~Oo0cOv0qO{*gO~P'vOo0cOv0qO{*gO!W&Xq~P'vOz-pO!W&Xq~Oo0cOv0qOz-pO!W&Xq~P'vOs-sO!T%dO!U%cOg&Oq!W&Oq![&Oqz&Oq~P!/jOa+QOo0cOv0qO![&Ty~P'vOz$ji![$ji~P%SOa+QOo0cOv0qO~P'vOV+UOo0cOv0qO~P'vOV+UOo0cOv0qO{&lq![&lq!m&lq%z&lq~P'vO{(kO![-xO!m-yO%z-wO~OV&OOo0cOv0qO#g%hq%[%hq%_%hq%z%hq~P'vO%uWO#g&ry%[&ry%_&ryg&ry~OV)`Oa)`O%uWO!W&ui~Ot-}OP#m!RV#m!Rf#m!Rh#m!Ro#m!Rs#m!Rv#m!R!P#m!R!Q#m!R!T#m!R!U#m!R!X#m!R!]#m!R!h#m!R!r#m!R!s#m!R!t#m!R!{#m!R!}#m!R#P#m!R#R#m!R#T#m!R#X#m!R#Z#m!R#^#m!R#_#m!R#a#m!R#c#m!R#l#m!R#o#m!R#s#m!R#u#m!R#z#m!R#}#m!R$P#m!R%X#m!R%o#m!R%p#m!R%t#m!R%u#m!R&Z#m!R&[#m!R&]#m!R&^#m!R&_#m!R&`#m!R&a#m!R&b#m!R&c#m!R&d#m!R&e#m!R&f#m!R&g#m!R&h#m!R&i#m!R&j#m!R%Z#m!R%_#m!R~Oo0cOv0qO{&xy~P'vOV*SOa*TO%q*UO%uWOg&yi~O$S-lO%Z.VO%_.VO~OV.aOh._O!X.^O!].`O!h.YO!s.[O!t.[O%p.XO%uWO&Z]O&[]O&]]O&^]O&_]O&`]O&a]O&b]O~Oo0cOv0qOz$lq!W$lq~P'vO{.fOz$lq!W$lq~Oo0cOv0qO{*gO!W&Xy~P'vOz.gO!W&Xy~Oo0cOv.kO~P'vOs-sO!T%dO!U%cOg&Oy!W&Oy![&Oyz&Oy~P!/jO{(kO![.nO~O{(kO![.nO!m.oO~OV*SOa*TO%q*UO%uWO~Oh.tO!f.rOz$TX#[$TX%j$TXg$TX~Os$TX{$TX!W$TX![$TX~P$-bO%o.vO%p.vOs$UXz$UX{$UX#[$UX%j$UX!W$UXg$UX![$UX~O!h.xO~Oz.|O#[/OO%j.yOs&|X{&|X!W&|Xg&|X~Oa/RO~P$)zOh.tOs&}Xz&}X{&}X#[&}X%j&}X!W&}Xg&}X![&}X~Os/VO{$jO~Oo0cOv0qOz$ly!W$ly~P'vOo0cOv0qO{*gO!W&X!R~P'vOz/ZO!W&X!R~Og&RXs&RX!T&RX!U&RX!W&RX![&RXz&RX~P!/jOs-sO!T%dO!U%cOg&Qa!W&Qa![&Qaz&Qa~O{(kO![/^O~O!f.rOh$[as$[az$[a{$[a#[$[a%j$[a!W$[ag$[a![$[a~O!h/eO~O%o.vO%p.vOs$Uaz$Ua{$Ua#[$Ua%j$Ua!W$Uag$Ua![$Ua~O%j.yOs$Yaz$Ya{$Ya#[$Ya!W$Yag$Ya![$Ya~Os&|a{&|a!W&|ag&|a~P$)nOz/jOs&|a{&|a!W&|ag&|a~O!W/mO~Og/mO~O{/oO~O![/pO~Oo0cOv0qO{*gO!W&X!Z~P'vO{/sO~O%z/tO~P$-bOz/uO#[/OO%j.yOg'PX~Oz/uOg'PX~Og/wO~O!h/xO~O#[/OOs%Saz%Sa{%Sa%j%Sa!W%Sag%Sa![%Sa~O#[/OO%j.yOs%Waz%Wa{%Wa!W%Wag%Wa~Os&|i{&|i!W&|ig&|i~P$)nOz/zO#[/OO%j.yO!['Oa~Og'Pa~P$)nOz0SOg'Pa~Oa0UO!['Oi~P$)zOz0WO!['Oi~Oz0WO#[/OO%j.yO!['Oi~O#[/OO%j.yOg$biz$bi~O%z0ZO~P$-bO#[/OO%j.yOg%Vaz%Va~Og'Pi~P$)nO{0^O~Oa0UO!['Oq~P$)zOz0`O!['Oq~O#[/OO%j.yOz%Ui![%Ui~Oa0UO~P$)zOa0UO!['Oy~P$)zO#[/OO%j.yOg$ciz$ci~O#[/OO%j.yOz%Uq![%Uq~Oz+aO#g%ha%[%ha%_%ha%z%ha~P%SOV&OOo0cOv0qO~P'vOn0hO~Oo0hO~P'vO{0iO~Ot0jO~P!/jO&]&Z&j&h&i&g&f&d&e&c&b&`&a&_&^&[%u~",
  goto: "!=j'QPPPPPP'RP'Z*s+[+t,_,y-fP.SP'Z.r.r'ZPPP'Z2[PPPPPP2[5PPP5PP7b7k=sPP=v>h>kPP'Z'ZPP>zPP'Z'ZPP'Z'Z'Z'Z'Z?O?w'ZP?zP@QDXGuGyPG|HWH['ZPPPH_Hk'RP'R'RP'RP'RP'RP'RP'R'R'RP'RPP'RPP'RP'RPHqH}IVPI^IdPI^PI^I^PPPI^PKrPK{LVL]KrPI^LfPI^PLmLsPLwM]MzNeLwLwNkNxLwLwLwLw! ^! d! g! l! o! y!!P!!]!!o!!u!#P!#V!#s!#y!$P!$Z!$a!$g!$y!%T!%Z!%a!%k!%q!%w!%}!&T!&Z!&e!&k!&u!&{!'U!'[!'k!'s!'}!(UPPPPPPPPPPP!([!(_!(e!(n!(x!)TPPPPPPPPPPPP!-u!/Z!3^!6oPP!6w!7W!7a!8Y!8P!8c!8i!8l!8o!8r!8z!9jPPPPPPPPPPPPPPPPP!9m!9q!9wP!:]!:a!:m!:v!;S!;j!;m!;p!;v!;|!<S!<VP!<_!<h!=d!=g]eOn#g$j)t,P'}`OTYZ[adnoprtxy}!P!Q!R!U!X!c!d!e!f!g!h!i!k!o!p!q!s!t!z#O#S#T#[#d#g#x#y#{#}$Q$e$g$h$j$q$}%S%Z%^%`%c%g%l%n%w%|&O&Z&_&h&j&k&u&x&|'P'W'Z'l'm'p'r's'w'|(O(S(W(](^(d(g(p(r(z(})^)e)g)k)l)p)t)z*O*Y*d*g*h*k*q*r*t*v*y*z*}+Q+U+V+Y+a+c+d+k+x+y,P,X,Y,],g,h,i,k,l,o,q,s,u,w,y,z-O-d-f-m-p-s.f.g/V/Z/s0c0d0e0f0h0i0j0k0l0n0r{!cQ#c#p$R$d$p%e%j%p%q&`'O'g(q(|)j*o*x+w,v0g}!dQ#c#p$R$d$p$u%e%j%p%q&`'O'g(q(|)j*o*x+w,v0g!P!eQ#c#p$R$d$p$u$v%e%j%p%q&`'O'g(q(|)j*o*x+w,v0g!R!fQ#c#p$R$d$p$u$v$w%e%j%p%q&`'O'g(q(|)j*o*x+w,v0g!T!gQ#c#p$R$d$p$u$v$w$x%e%j%p%q&`'O'g(q(|)j*o*x+w,v0g!V!hQ#c#p$R$d$p$u$v$w$x$y%e%j%p%q&`'O'g(q(|)j*o*x+w,v0g!Z!hQ!n#c#p$R$d$p$u$v$w$x$y$z%e%j%p%q&`'O'g(q(|)j*o*x+w,v0g'}TOTYZ[adnoprtxy}!P!Q!R!U!X!c!d!e!f!g!h!i!k!o!p!q!s!t!z#O#S#T#[#d#g#x#y#{#}$Q$e$g$h$j$q$}%S%Z%^%`%c%g%l%n%w%|&O&Z&_&h&j&k&u&x&|'P'W'Z'l'm'p'r's'w'|(O(S(W(](^(d(g(p(r(z(})^)e)g)k)l)p)t)z*O*Y*d*g*h*k*q*r*t*v*y*z*}+Q+U+V+Y+a+c+d+k+x+y,P,X,Y,],g,h,i,k,l,o,q,s,u,w,y,z-O-d-f-m-p-s.f.g/V/Z/s0c0d0e0f0h0i0j0k0l0n0r&eVOYZ[dnprxy}!P!Q!U!i!k!o!p!q!s!t#[#d#g#y#{#}$Q$h$j$}%S%Z%^%`%g%l%n%w%|&Z&_&j&k&u&x'P'W'Z'l'm'p'r's'w(O(W(^(d(g(p(r(z)^)e)g)p)t)z*O*Y*d*g*h*k*q*r*t*v*y*z*}+U+V+Y+a+d+k,P,X,Y,],g,h,i,k,l,o,q,s,u,w,y,z-O-d-f-m-p-s.f.g/V/Z/s0c0d0e0f0h0i0j0k0n0r%oXOYZ[dnrxy}!P!Q!U!i!k#[#d#g#y#{#}$Q$h$j$}%S%^%`%g%l%n%w%|&Z&_&j&k&u&x'P'W'Z'l'm'p'r's'w(O(W(^(d(g(p(r(z)^)e)g)p)t)z*O*Y*d*g*h*k*q*t*v*y*z*}+U+V+Y+a+d+k,P,X,Y,],g,h,i,k,l,o,s,u,w,y,z-O-d-f-m-p.f.g/V/Z0i0j0kQ#vqQ/[.kR0o0q't`OTYZ[adnoprtxy}!P!Q!R!U!X!c!d!e!f!g!h!k!o!p!q!s!t!z#O#S#T#[#d#g#x#y#{#}$Q$e$g$h$j$q$}%S%Z%^%`%c%g%l%n%w%|&O&Z&_&h&j&k&u&x&|'P'W'Z'l'p'r's'w'|(O(S(W(](^(d(g(p(r(z(})^)e)g)k)l)p)t)z*O*Y*g*h*k*q*r*t*v*y*z*}+Q+U+V+Y+a+c+d+k+x+y,P,X,Y,],h,i,k,l,o,q,s,u,w,y,z-O-d-f-m-p-s.f.g/V/Z/s0c0d0e0f0h0i0j0k0l0n0rh#jhz{$W$Z&l&q)S)X+f+g-RW#rq&].k0qQ$]|Q$a!OQ$n!VQ$o!WW$|!i'm*d,gS&[#s#tQ'S$iQ(s&UQ)U&nU)Y&s)Z+jW)a&w+m-T-{Q*Q']W*R'_,`-h.TQ+l)`S,_*S*TQ-Q+eQ-_,TQ-c,WQ.R-al.W-l.^._.a.z.|/R/j/o/t/y0U0Z0^Q/S.`Q/a.tQ/l/OU0P/u0S0[X0V/z0W0_0`R&Z#r!_!wYZ!P!Q!k%S%`%g'p'r's(O(W)g*g*h*k*q*t*v,h,i,k,l,o-m-p.f.g/ZR%^!vQ!{YQ%x#[Q&d#}Q&g$QR,{+YT.j-s/s!Y!jQ!n#c#p$R$d$p$u$v$w$x$y$z%e%j%p%q&`'O'g(q(|)j*o*x+w,v0gQ&X#kQ'c$oR*^'dR'l$|Q%V!mR/_.r'|_OTYZ[adnoprtxy}!P!Q!R!U!X!c!d!e!f!g!h!i!k!o!p!q!s!t!z#O#S#T#[#d#g#x#y#{#}$Q$e$g$h$j$q$}%S%Z%^%`%c%g%l%n%w%|&O&Z&_&h&j&k&u&x&|'P'W'Z'l'm'p'r's'w'|(O(S(W(](^(d(g(p(r(z(})^)e)g)k)l)p)t)z*O*Y*d*g*h*k*q*r*t*v*y*z*}+Q+U+V+Y+a+c+d+k+x+y,P,X,Y,],g,h,i,k,l,o,q,s,u,w,y,z-O-d-f-m-p-s.f.g/V/Z/s0c0d0e0f0h0i0j0k0l0n0rS#a_#b!P.[-l.^._.`.a.t.z.|/R/j/o/t/u/y/z0S0U0W0Z0[0^0_0`'|_OTYZ[adnoprtxy}!P!Q!R!U!X!c!d!e!f!g!h!i!k!o!p!q!s!t!z#O#S#T#[#d#g#x#y#{#}$Q$e$g$h$j$q$}%S%Z%^%`%c%g%l%n%w%|&O&Z&_&h&j&k&u&x&|'P'W'Z'l'm'p'r's'w'|(O(S(W(](^(d(g(p(r(z(})^)e)g)k)l)p)t)z*O*Y*d*g*h*k*q*r*t*v*y*z*}+Q+U+V+Y+a+c+d+k+x+y,P,X,Y,],g,h,i,k,l,o,q,s,u,w,y,z-O-d-f-m-p-s.f.g/V/Z/s0c0d0e0f0h0i0j0k0l0n0rT#a_#bT#^^#_R(o%xa(l%x(n(o+`,{-y-z.oT+[(k+]R-z,{Q$PsQ+l)aQ,^*RR-e,_X#}s$O$P&fQ&y$aQ'a$nQ'd$oR)s'SQ)b&wV-S+m-T-{ZgOn$j)t,PXkOn)t,PQ$k!TQ&z$bQ&{$cQ'^$mQ'b$oQ)q'RQ)x'WQ){'XQ)|'YQ*Z'`S*]'c'dQ+s)gQ+u)hQ+v)iQ+z)oS+|)r*[Q,Q)vQ,R)wS,S)y)zQ,d*^Q-V+rQ-W+tQ-Y+{S-Z+},OQ-`,UQ-b,VQ-|-XQ.O-[Q.P-^Q.Q-_Q.p-}Q.q.RQ/W.dR/r/XWkOn)t,PR#mjQ'`$nS)r'S'aR,O)sQ,]*RR-f,^Q*['`Q+})rR-[,OZiOjn)t,PQ'f$pR*`'gT-j,e-ku.c-l.^._.a.t.z.|/R/j/o/t/u/y0S0U0Z0[0^t.c-l.^._.a.t.z.|/R/j/o/t/u/y0S0U0Z0[0^Q/S.`X0V/z0W0_0`!P.Z-l.^._.`.a.t.z.|/R/j/o/t/u/y/z0S0U0W0Z0[0^0_0`Q.w.YR/f.xg.z.].{/b/i/n/|0O0Q0]0a0bu.b-l.^._.a.t.z.|/R/j/o/t/u/y0S0U0Z0[0^X.u.W.b/a0PR/c.tV0R/u0S0[R/X.dQnOS#on,PR,P)tQ&^#uR(x&^S%m#R#wS(_%m(bT(b%p&`Q%a!yQ%h!}W(P%a%h(U(YQ(U%eR(Y%jQ&i$RR)O&iQ(e%qQ*{(`T+R(e*{Q'n%OR*e'nS'q%R%SY*i'q*j,m-q.hU*j'r's'tU,m*k*l*mS-q,n,oR.h-rQ#Y]R%t#YQ#_^R%y#_Q(h%vS+W(h+XR+X(iQ+](kR,|+]Q#b_R%{#bQ#ebQ%}#cW&Q#e%}({+bQ({&cR+b0gQ$OsS&e$O&fR&f$PQ&v$_R)_&vQ&V#jR(t&VQ&m$VS)T&m+hR+h)UQ$Z{R&p$ZQ&t$]R)[&tQ+n)bR-U+nQ#hfR&S#hQ)f&zR+q)fQ&}$dS)m&})nR)n'OQ'V$kR)u'VQ'[$lS*P'[,ZR,Z*QQ,a*VR-i,aWjOn)t,PR#ljQ-k,eR.U-kd.{.]/b/i/n/|0O0Q0]0a0bR/h.{U.s.W/a0PR/`.sQ/{/nS0X/{0YR0Y/|S/v/b/cR0T/vQ.}.]R/k.}R!ZPXmOn)t,PWlOn)t,PR'T$jYfOn$j)t,PR&R#g[sOn#g$j)t,PR&d#}&dQOYZ[dnprxy}!P!Q!U!i!k!o!p!q!s!t#[#d#g#y#{#}$Q$h$j$}%S%Z%^%`%g%l%n%w%|&Z&_&j&k&u&x'P'W'Z'l'm'p'r's'w(O(W(^(d(g(p(r(z)^)e)g)p)t)z*O*Y*d*g*h*k*q*r*t*v*y*z*}+U+V+Y+a+d+k,P,X,Y,],g,h,i,k,l,o,q,s,u,w,y,z-O-d-f-m-p-s.f.g/V/Z/s0c0d0e0f0h0i0j0k0n0rQ!nTQ#caQ#poU$Rt%c(SS$d!R$gQ$p!XQ$u!cQ$v!dQ$w!eQ$x!fQ$y!gQ$z!hQ%e!zQ%j#OQ%p#SQ%q#TQ&`#xQ'O$eQ'g$qQ(q&OU(|&h(}+cW)j&|)l+x+yQ*o'|Q*x(]Q+w)kQ,v+QR0g0lQ!yYQ!}ZQ$b!PQ$c!QQ%R!kQ't%S^'{%`%g(O(W*q*t*v^*f'p*h,k,l-p.g/ZQ*l'rQ*m'sQ+t)gQ,j*gQ,n*kQ-n,hQ-o,iQ-r,oQ.e-mR/Y.f[bOn#g$j)t,P!^!vYZ!P!Q!k%S%`%g'p'r's(O(W)g*g*h*k*q*t*v,h,i,k,l,o-m-p.f.g/ZQ#R[Q#fdS#wrxQ$UyW$_}$Q'P)pS$l!U$hW${!i'm*d,gS%v#[+Y`&P#d%|(p(r(z+a-O0kQ&a#yQ&b#{Q&c#}Q'j$}Q'z%^W([%l(^*y*}Q(`%nQ(i%wQ(v&ZS(y&_0iQ)P&jQ)Q&kU)]&u)^+kQ)d&xQ)y'WY)}'Z*O,X,Y-dQ*b'lS*n'w0jW+P(d*z,s,wW+T(g+V,y,zQ+p)eQ,U)zQ,c*YQ,x+UQ-P+dQ-e,]Q-v,uQ.S-fR/q/VhUOn#d#g$j%|&_'w(p(r)t,P%U!uYZ[drxy}!P!Q!U!i!k#[#y#{#}$Q$h$}%S%^%`%g%l%n%w&Z&j&k&u&x'P'W'Z'l'm'p'r's(O(W(^(d(g(z)^)e)g)p)z*O*Y*d*g*h*k*q*t*v*y*z*}+U+V+Y+a+d+k,X,Y,],g,h,i,k,l,o,s,u,w,y,z-O-d-f-m-p.f.g/V/Z0i0j0kQ#qpW%W!o!s0d0nQ%X!pQ%Y!qQ%[!tQ%f0cS'v%Z0hQ'x0eQ'y0fQ,p*rQ-u,qS.i-s/sR0p0rU#uq.k0qR(w&][cOn#g$j)t,PZ!xY#[#}$Q+YQ#W[Q#zrR$TxQ%b!yQ%i!}Q%o#RQ'j${Q(V%eQ(Z%jQ(c%pQ(f%qQ*|(`Q,f*bQ-t,pQ.m-uR/].lQ$StQ(R%cR*s(SQ.l-sR/}/sR#QZR#V[R%Q!iQ%O!iV*c'm*d,g!Z!lQ!n#c#p$R$d$p$u$v$w$x$y$z%e%j%p%q&`'O'g(q(|)j*o*x+w,v0gR%T!kT#]^#_Q%x#[R,{+YQ(m%xS+_(n(oQ,}+`Q-x,{S.n-y-zR/^.oT+Z(k+]Q$`}Q&g$QQ)o'PR+{)pQ$XzQ)W&qR+i)XQ$XzQ&o$WQ)W&qR+i)XQ#khW$Vz$W&q)XQ$[{Q&r$ZZ)R&l)S+f+g-RR$^|R)c&wXlOn)t,PQ$f!RR'Q$gQ$m!UR'R$hR*X'_Q*V'_V-g,`-h.TQ.d-lQ/P.^R/Q._U.]-l.^._Q/U.aQ/b.tQ/g.zU/i.|/j/yQ/n/RQ/|/oQ0O/tU0Q/u0S0[Q0]0UQ0a0ZR0b0^R/T.`R/d.t",
  nodeNames: "\u26A0 print Escape { Comment Script AssignStatement * BinaryExpression BitOp BitOp BitOp BitOp ArithOp ArithOp @ ArithOp ** UnaryExpression ArithOp BitOp AwaitExpression await ) ( ParenthesizedExpression BinaryExpression or and CompareOp in not is UnaryExpression ConditionalExpression if else LambdaExpression lambda ParamList VariableName AssignOp , : NamedExpression AssignOp YieldExpression yield from TupleExpression ComprehensionExpression async for LambdaExpression ] [ ArrayExpression ArrayComprehensionExpression } { DictionaryExpression DictionaryComprehensionExpression SetExpression SetComprehensionExpression CallExpression ArgList AssignOp MemberExpression . PropertyName Number String FormatString FormatReplacement FormatSelfDoc FormatConversion FormatSpec FormatReplacement FormatSelfDoc ContinuedString Ellipsis None Boolean TypeDef AssignOp UpdateStatement UpdateOp ExpressionStatement DeleteStatement del PassStatement pass BreakStatement break ContinueStatement continue ReturnStatement return YieldStatement PrintStatement RaiseStatement raise ImportStatement import as ScopeStatement global nonlocal AssertStatement assert TypeDefinition type TypeParamList TypeParam StatementGroup ; IfStatement Body elif WhileStatement while ForStatement TryStatement try except finally WithStatement with FunctionDefinition def ParamList AssignOp TypeDef ClassDefinition class DecoratedStatement Decorator At MatchStatement match MatchBody MatchClause case CapturePattern LiteralPattern ArithOp ArithOp AsPattern OrPattern LogicOp AttributePattern SequencePattern MappingPattern StarPattern ClassPattern PatternArgList KeywordPattern KeywordPattern Guard",
  maxTerm: 277,
  context: trackIndent,
  nodeProps: [
    ["isolate", -5, 4, 71, 72, 73, 77, ""],
    ["group", -15, 6, 85, 87, 88, 90, 92, 94, 96, 98, 99, 100, 102, 105, 108, 110, "Statement Statement", -22, 8, 18, 21, 25, 40, 49, 50, 56, 57, 60, 61, 62, 63, 64, 67, 70, 71, 72, 79, 80, 81, 82, "Expression", -10, 114, 116, 119, 121, 122, 126, 128, 133, 135, 138, "Statement", -9, 143, 144, 147, 148, 150, 151, 152, 153, 154, "Pattern"],
    ["openedBy", 23, "(", 54, "[", 58, "{"],
    ["closedBy", 24, ")", 55, "]", 59, "}"]
  ],
  propSources: [pythonHighlighting],
  skippedNodes: [0, 4],
  repeatNodeCount: 34,
  tokenData: "!2|~R!`OX%TXY%oY[%T[]%o]p%Tpq%oqr'ars)Yst*xtu%Tuv,dvw-hwx.Uxy/tyz0[z{0r{|2S|}2p}!O3W!O!P4_!P!Q:Z!Q!R;k!R![>_![!]Do!]!^Es!^!_FZ!_!`Gk!`!aHX!a!b%T!b!cIf!c!dJU!d!eK^!e!hJU!h!i!#f!i!tJU!t!u!,|!u!wJU!w!x!.t!x!}JU!}#O!0S#O#P&o#P#Q!0j#Q#R!1Q#R#SJU#S#T%T#T#UJU#U#VK^#V#YJU#Y#Z!#f#Z#fJU#f#g!,|#g#iJU#i#j!.t#j#oJU#o#p!1n#p#q!1s#q#r!2a#r#s!2f#s$g%T$g;'SJU;'S;=`KW<%lOJU`%YT&n`O#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%T`%lP;=`<%l%To%v]&n`%c_OX%TXY%oY[%T[]%o]p%Tpq%oq#O%T#O#P&o#P#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%To&tX&n`OY%TYZ%oZ]%T]^%o^#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tc'f[&n`O!_%T!_!`([!`#T%T#T#U(r#U#f%T#f#g(r#g#h(r#h#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tc(cTmR&n`O#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tc(yT!mR&n`O#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tk)aV&n`&[ZOr%Trs)vs#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tk){V&n`Or%Trs*bs#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tk*iT&n`&^ZO#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%To+PZS_&n`OY*xYZ%TZ]*x]^%T^#o*x#o#p+r#p#q*x#q#r+r#r;'S*x;'S;=`,^<%lO*x_+wTS_OY+rZ]+r^;'S+r;'S;=`,W<%lO+r_,ZP;=`<%l+ro,aP;=`<%l*xj,kV%rQ&n`O!_%T!_!`-Q!`#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tj-XT!xY&n`O#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tj-oV%lQ&n`O!_%T!_!`-Q!`#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tk.]V&n`&ZZOw%Twx.rx#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tk.wV&n`Ow%Twx/^x#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tk/eT&n`&]ZO#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tk/{ThZ&n`O#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tc0cTgR&n`O#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tk0yXVZ&n`Oz%Tz{1f{!_%T!_!`-Q!`#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tk1mVaR&n`O!_%T!_!`-Q!`#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tk2ZV%oZ&n`O!_%T!_!`-Q!`#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tc2wTzR&n`O#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%To3_W%pZ&n`O!_%T!_!`-Q!`!a3w!a#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Td4OT&{S&n`O#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tk4fX!fQ&n`O!O%T!O!P5R!P!Q%T!Q![6T![#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tk5WV&n`O!O%T!O!P5m!P#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tk5tT!rZ&n`O#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Ti6[a!hX&n`O!Q%T!Q![6T![!g%T!g!h7a!h!l%T!l!m9s!m#R%T#R#S6T#S#X%T#X#Y7a#Y#^%T#^#_9s#_#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Ti7fZ&n`O{%T{|8X|}%T}!O8X!O!Q%T!Q![8s![#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Ti8^V&n`O!Q%T!Q![8s![#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Ti8z]!hX&n`O!Q%T!Q![8s![!l%T!l!m9s!m#R%T#R#S8s#S#^%T#^#_9s#_#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Ti9zT!hX&n`O#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tk:bX%qR&n`O!P%T!P!Q:}!Q!_%T!_!`-Q!`#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tj;UV%sQ&n`O!_%T!_!`-Q!`#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Ti;ro!hX&n`O!O%T!O!P=s!P!Q%T!Q![>_![!d%T!d!e?q!e!g%T!g!h7a!h!l%T!l!m9s!m!q%T!q!rA]!r!z%T!z!{Bq!{#R%T#R#S>_#S#U%T#U#V?q#V#X%T#X#Y7a#Y#^%T#^#_9s#_#c%T#c#dA]#d#l%T#l#mBq#m#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Ti=xV&n`O!Q%T!Q![6T![#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Ti>fc!hX&n`O!O%T!O!P=s!P!Q%T!Q![>_![!g%T!g!h7a!h!l%T!l!m9s!m#R%T#R#S>_#S#X%T#X#Y7a#Y#^%T#^#_9s#_#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Ti?vY&n`O!Q%T!Q!R@f!R!S@f!S#R%T#R#S@f#S#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Ti@mY!hX&n`O!Q%T!Q!R@f!R!S@f!S#R%T#R#S@f#S#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%TiAbX&n`O!Q%T!Q!YA}!Y#R%T#R#SA}#S#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%TiBUX!hX&n`O!Q%T!Q!YA}!Y#R%T#R#SA}#S#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%TiBv]&n`O!Q%T!Q![Co![!c%T!c!iCo!i#R%T#R#SCo#S#T%T#T#ZCo#Z#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%TiCv]!hX&n`O!Q%T!Q![Co![!c%T!c!iCo!i#R%T#R#SCo#S#T%T#T#ZCo#Z#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%ToDvV{_&n`O!_%T!_!`E]!`#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%TcEdT%{R&n`O#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%TkEzT#gZ&n`O#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%TkFbXmR&n`O!^%T!^!_F}!_!`([!`!a([!a#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%TjGUV%mQ&n`O!_%T!_!`-Q!`#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%TkGrV%zZ&n`O!_%T!_!`([!`#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%TkH`WmR&n`O!_%T!_!`([!`!aHx!a#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%TjIPV%nQ&n`O!_%T!_!`-Q!`#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%TkIoV_Q#}P&n`O!_%T!_!`-Q!`#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%ToJ_]&n`&YS%uZO!Q%T!Q![JU![!c%T!c!}JU!}#R%T#R#SJU#S#T%T#T#oJU#p#q%T#r$g%T$g;'SJU;'S;=`KW<%lOJUoKZP;=`<%lJUoKge&n`&YS%uZOr%Trs)Ysw%Twx.Ux!Q%T!Q![JU![!c%T!c!tJU!t!uLx!u!}JU!}#R%T#R#SJU#S#T%T#T#fJU#f#gLx#g#oJU#p#q%T#r$g%T$g;'SJU;'S;=`KW<%lOJUoMRa&n`&YS%uZOr%TrsNWsw%Twx! vx!Q%T!Q![JU![!c%T!c!}JU!}#R%T#R#SJU#S#T%T#T#oJU#p#q%T#r$g%T$g;'SJU;'S;=`KW<%lOJUkN_V&n`&`ZOr%TrsNts#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%TkNyV&n`Or%Trs! `s#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tk! gT&n`&bZO#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tk! }V&n`&_ZOw%Twx!!dx#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tk!!iV&n`Ow%Twx!#Ox#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tk!#VT&n`&aZO#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%To!#oe&n`&YS%uZOr%Trs!%Qsw%Twx!&px!Q%T!Q![JU![!c%T!c!tJU!t!u!(`!u!}JU!}#R%T#R#SJU#S#T%T#T#fJU#f#g!(`#g#oJU#p#q%T#r$g%T$g;'SJU;'S;=`KW<%lOJUk!%XV&n`&dZOr%Trs!%ns#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tk!%sV&n`Or%Trs!&Ys#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tk!&aT&n`&fZO#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tk!&wV&n`&cZOw%Twx!'^x#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tk!'cV&n`Ow%Twx!'xx#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tk!(PT&n`&eZO#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%To!(ia&n`&YS%uZOr%Trs!)nsw%Twx!+^x!Q%T!Q![JU![!c%T!c!}JU!}#R%T#R#SJU#S#T%T#T#oJU#p#q%T#r$g%T$g;'SJU;'S;=`KW<%lOJUk!)uV&n`&hZOr%Trs!*[s#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tk!*aV&n`Or%Trs!*vs#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tk!*}T&n`&jZO#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tk!+eV&n`&gZOw%Twx!+zx#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tk!,PV&n`Ow%Twx!,fx#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tk!,mT&n`&iZO#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%To!-Vi&n`&YS%uZOr%TrsNWsw%Twx! vx!Q%T!Q![JU![!c%T!c!dJU!d!eLx!e!hJU!h!i!(`!i!}JU!}#R%T#R#SJU#S#T%T#T#UJU#U#VLx#V#YJU#Y#Z!(`#Z#oJU#p#q%T#r$g%T$g;'SJU;'S;=`KW<%lOJUo!.}a&n`&YS%uZOr%Trs)Ysw%Twx.Ux!Q%T!Q![JU![!c%T!c!}JU!}#R%T#R#SJU#S#T%T#T#oJU#p#q%T#r$g%T$g;'SJU;'S;=`KW<%lOJUk!0ZT!XZ&n`O#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tc!0qT!WR&n`O#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%Tj!1XV%kQ&n`O!_%T!_!`-Q!`#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%T~!1sO!]~k!1zV%jR&n`O!_%T!_!`-Q!`#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%T~!2fO![~i!2mT%tX&n`O#o%T#p#q%T#r;'S%T;'S;=`%i<%lO%T",
  tokenizers: [legacyPrint, indentation, newlines, strings, 0, 1, 2, 3, 4],
  topRules: { "Script": [0, 5] },
  specialized: [{ term: 221, get: (value) => spec_identifier[value] || -1 }],
  tokenPrec: 7668
});

// src/core/workspaceIndex.ts
var WorkspaceIndex = class {
  static {
    this.steps = /* @__PURE__ */ new Map();
  }
  static async indexWorkspace() {
    const config = vscode2.workspace.getConfiguration("wpipe");
    const userExcludes = config.get("excludePaths", []);
    const maxFiles = config.get("maxSearchFiles", 500);
    const defaultExcludes = [
      "**/node_modules/**",
      "**/.venv/**",
      "**/venv/**",
      "**/.env/**",
      "**/env/**",
      "**/.conda/**",
      "**/conda/**",
      "**/site-packages/**",
      "**/wpipe/wpipe/**",
      "**/__pycache__/**",
      "**/.pytest_cache/**",
      "**/.mypy_cache/**",
      "**/.ruff_cache/**",
      "**/.tox/**",
      "**/build/**",
      "**/dist/**",
      "**/*.egg-info/**"
    ];
    const combinedExcludes = Array.from(/* @__PURE__ */ new Set([...defaultExcludes, ...userExcludes]));
    const excludePattern = `{${combinedExcludes.join(",")}}`;
    const files = await vscode2.workspace.findFiles("**/*.py", excludePattern, maxFiles);
    const newSteps = /* @__PURE__ */ new Map();
    for (const f of files) {
      try {
        const contentData = await vscode2.workspace.fs.readFile(f);
        if (contentData.length > 5e5) continue;
        const content2 = new TextDecoder().decode(contentData);
        const tree = parser.parse(content2);
        tree.iterate({
          enter: (node) => {
            if (node.name === "Decorator") {
              const decText = content2.substring(node.from, node.to);
              if (decText.startsWith("@step")) {
                let name2 = "";
                let version = "v1.0";
                let description = "";
                const nameMatch = decText.match(/name\s*=\s*['"](.*?)['"]/);
                if (nameMatch) name2 = nameMatch[1];
                const verMatch = decText.match(/version\s*=\s*['"](.*?)['"]/);
                if (verMatch) version = verMatch[1];
                const descMatch = decText.match(/description\s*=\s*['"](.*?)['"]/);
                if (descMatch) description = descMatch[1];
                if (!name2 && node.node.parent) {
                  let funcDef = node.node.parent.getChild("FunctionDefinition") || node.node.parent.getChild("ClassDefinition");
                  if (funcDef) {
                    let varName = funcDef.getChild("VariableName");
                    if (varName) name2 = content2.substring(varName.from, varName.to);
                  }
                }
                if (name2) {
                  const line = content2.substring(0, node.from).split("\n").length - 1;
                  newSteps.set(name2, { name: name2, version, filePath: f.fsPath, line, description });
                }
              }
            }
          }
        });
      } catch (e) {
      }
    }
    this.steps = newSteps;
  }
  static getStep(name2) {
    return this.steps.get(name2);
  }
  static getAllSteps() {
    return Array.from(this.steps.values());
  }
};

// src/providers/stepProvider.ts
var WPipeStepProvider = class {
  constructor() {
    this._onDidChangeTreeData = new vscode3.EventEmitter();
    this.onDidChangeTreeData = this._onDidChangeTreeData.event;
  }
  refresh() {
    this._onDidChangeTreeData.fire();
  }
  getTreeItem(e) {
    return e;
  }
  async getChildren(element) {
    if (!element) {
      return [
        new vscode3.TreeItem("\u{1F6E0}\uFE0F Workspace Steps", vscode3.TreeItemCollapsibleState.Expanded),
        new vscode3.TreeItem("\u{1F4E6} Official Library", vscode3.TreeItemCollapsibleState.Collapsed),
        new vscode3.TreeItem("\u{1F91D} Community Plugins", vscode3.TreeItemCollapsibleState.Collapsed)
      ];
    }
    if (element instanceof CategoryItem) {
      return this.getCategoryChildren(element.repo, element.path);
    }
    const label = element.label;
    if (label.includes("Workspace")) {
      return this.searchWorkspace();
    }
    if (label.includes("Official")) {
      return this.getCategoryChildren("Official", []);
    }
    if (label.includes("Community")) {
      return this.getCategoryChildren("Community", []);
    }
    return [];
  }
  /**
   * Resolves the child categories and library items for a given path and repository.
   */
  getCategoryChildren(repo, categoryPath) {
    const steps = CatalogManager.getSteps().filter((s) => s.repo === repo);
    const subcategoriesSet = /* @__PURE__ */ new Set();
    const directLibraryItems = [];
    for (const step of steps) {
      let catSeq = [step.category, step.subcategory1, step.subcategory2, step.subcategory3].map((s) => s?.trim()).filter(Boolean);
      if (catSeq.length === 0) {
        catSeq = ["General"];
      }
      if (categoryPath.length <= catSeq.length && categoryPath.every((val, idx) => catSeq[idx] === val)) {
        if (catSeq.length === categoryPath.length) {
          directLibraryItems.push(new LibraryItem(step));
        } else {
          const nextSubcat = catSeq[categoryPath.length];
          subcategoriesSet.add(nextSubcat);
        }
      }
    }
    const categoryItems = Array.from(subcategoriesSet).map(
      (subcat) => new CategoryItem(subcat, repo, [...categoryPath, subcat])
    );
    categoryItems.sort((a, b) => a.label.localeCompare(b.label));
    directLibraryItems.sort((a, b) => a.label.localeCompare(b.label));
    return [...categoryItems, ...directLibraryItems];
  }
  async searchWorkspace() {
    await WorkspaceIndex.indexWorkspace();
    return WorkspaceIndex.getAllSteps().map((s) => new StepItem(s.name, s.filePath, s.line));
  }
};
var StepItem = class extends vscode3.TreeItem {
  constructor(label, filePath, line) {
    super(label);
    this.filePath = filePath;
    this.line = line;
    this.funcName = "";
    this.iconPath = new vscode3.ThemeIcon("rocket");
    this.description = label;
    this.contextValue = "workspaceStep";
    this.command = { command: "wpipeSteps.openFile", title: "Open", arguments: [filePath, line] };
  }
};
var LibraryItem = class extends vscode3.TreeItem {
  constructor(step) {
    super(step.name);
    this.step = step;
    this.iconPath = new vscode3.ThemeIcon("cloud");
    this.description = step.version ? `v${step.version}` : step.namespace;
    const tooltip = new vscode3.MarkdownString();
    tooltip.isTrusted = true;
    tooltip.appendMarkdown(`### \u{1F4E6} ${step.name} 
`);
    if (step.version) tooltip.appendMarkdown(`*Version: ${step.version}*

`);
    if (step.description) {
      tooltip.appendMarkdown(`> ${step.description}

`);
    }
    tooltip.appendMarkdown(`---
`);
    tooltip.appendMarkdown(`**Author:** ${step.author || "Official"}

`);
    tooltip.appendMarkdown(`**Repo:** ${step.repo}

`);
    tooltip.appendMarkdown(`**Module:** \`${step.namespace}\`

`);
    if (step.requirements) {
      tooltip.appendMarkdown(`**Requirements:** \`${step.requirements}\`

`);
    }
    if (step.how_to_use) {
      tooltip.appendMarkdown(`**Usage:**
\`\`\`python
${step.how_to_use}
\`\`\`

`);
    }
    if (step.examples) {
      tooltip.appendMarkdown(`[Explore Examples](${step.examples})

`);
    }
    tooltip.appendMarkdown(`---
*Click to insert import and usage.*`);
    this.tooltip = tooltip;
    this.contextValue = "libraryStep";
    this.command = { command: "wpipeSteps.insertStep", title: "Insert", arguments: [step] };
  }
};
var CategoryItem = class extends vscode3.TreeItem {
  constructor(label, repo, path5) {
    super(label, vscode3.TreeItemCollapsibleState.Collapsed);
    this.repo = repo;
    this.path = path5;
    this.iconPath = new vscode3.ThemeIcon("folder");
    this.contextValue = "categoryItem";
  }
};

// src/webviews/dagPanel.ts
var vscode5 = __toESM(require("vscode"));
var path = __toESM(require("path"));

// src/core/config.ts
var vscode4 = __toESM(require("vscode"));
var ConfigManager = class {
  /**
   * Obtiene una configuración priorizando un archivo local 'wpipe.config.json' 
   * en la raíz del workspace, y cayendo de vuelta a las configuraciones de VS Code.
   */
  static async getSetting(key, defaultValue) {
    const workspaceFolders = vscode4.workspace.workspaceFolders;
    if (workspaceFolders) {
      const configPath = vscode4.Uri.joinPath(workspaceFolders[0].uri, "wpipe.config.json");
      try {
        const data = await vscode4.workspace.fs.readFile(configPath);
        const config = JSON.parse(new TextDecoder().decode(data));
        if (config[key] !== void 0) {
          return config[key];
        }
      } catch (e) {
      }
    }
    const vscodeConfig = vscode4.workspace.getConfiguration("wpipe");
    return vscodeConfig.get(key, defaultValue);
  }
  /**
   * Indica si la creación de archivos de respaldo (.wpipe.mermaid) está habilitada.
   */
  static async isBackupEnabled() {
    return await this.getSetting("enableBackupFile", true);
  }
};

// src/webviews/dagPanel.ts
var DAGPanel = class _DAGPanel {
  constructor(p, doc) {
    this._disposables = [];
    this._panel = p;
    this._panel.onDidDispose(() => {
      _DAGPanel.currentPanel = void 0;
    }, null, this._disposables);
    this._update(doc, true);
    this._panel.webview.onDidReceiveMessage(async (message) => {
      if (message.command === "downloadImage") {
        const saveUri = await vscode5.window.showSaveDialog({
          defaultUri: vscode5.Uri.file(message.fileName),
          filters: message.format === "png" ? { "PNG Image": ["png"] } : { "SVG Image": ["svg"] }
        });
        if (saveUri) {
          let data;
          if (message.format === "png") {
            const base64Data = message.content.replace(/^data:image\/png;base64,/, "");
            data = Buffer.from(base64Data, "base64");
          } else {
            data = new TextEncoder().encode(message.content);
          }
          await vscode5.workspace.fs.writeFile(saveUri, data);
          vscode5.window.showInformationMessage(`\u2705 DAG exported as ${message.format.toUpperCase()} successfully.`);
        }
      } else if (message.command === "gotoLine") {
        const line = parseInt(message.line);
        if (!isNaN(line)) {
          const editor = vscode5.window.activeTextEditor;
          if (editor && editor.document === doc) {
            const pos = new vscode5.Position(line, 0);
            editor.selection = new vscode5.Selection(pos, pos);
            editor.revealRange(new vscode5.Range(pos, pos), vscode5.TextEditorRevealType.InCenter);
          } else {
            const newDoc = await vscode5.workspace.openTextDocument(doc.uri);
            const newEditor = await vscode5.window.showTextDocument(newDoc);
            const pos = new vscode5.Position(line, 0);
            newEditor.selection = new vscode5.Selection(pos, pos);
            newEditor.revealRange(new vscode5.Range(pos, pos), vscode5.TextEditorRevealType.InCenter);
          }
        }
      }
    }, null, this._disposables);
    vscode5.workspace.onDidSaveTextDocument((e) => {
      if (e === doc) this._update(doc, true);
    }, null, this._disposables);
    vscode5.window.onDidChangeActiveTextEditor((e) => {
      if (e && e.document.languageId === "python") this._update(e.document, false);
    }, null, this._disposables);
  }
  static async createOrShow(uri, doc) {
    if (_DAGPanel.currentPanel) {
      _DAGPanel.currentPanel._panel.reveal();
      await _DAGPanel.currentPanel._update(doc, true);
      return;
    }
    const p = vscode5.window.createWebviewPanel("wpipeDAG", "WPipe Analysis", vscode5.ViewColumn.Two, {
      enableScripts: true,
      retainContextWhenHidden: true
    });
    _DAGPanel.currentPanel = new _DAGPanel(p, doc);
  }
  highlightNodes(nodeNames, status) {
    this._panel.webview.postMessage({
      command: "highlightNodes",
      nodes: nodeNames,
      status
    });
  }
  async _update(doc, forceBackup = false) {
    const fileName = path.basename(doc.uri.fsPath);
    const res = this.parse(doc, fileName);
    if (forceBackup && await ConfigManager.isBackupEnabled()) {
      try {
        const dir = path.dirname(doc.uri.fsPath);
        const base = path.basename(doc.uri.fsPath, path.extname(doc.uri.fsPath));
        const mdPath = path.join(dir, `${base}.wpipe.mermaid`);
        const content2 = `%% Generated by WPipe Tools
${res.graph}`;
        await vscode5.workspace.fs.writeFile(vscode5.Uri.file(mdPath), new TextEncoder().encode(content2));
      } catch (e) {
      }
    }
    this._panel.webview.html = this._getHtml(fileName, res.graph, res.stats, res.bigO, res.suggestions);
  }
  _getHtml(fileName, graph, stats, bigO, suggestions = []) {
    const now = (/* @__PURE__ */ new Date()).toLocaleTimeString();
    const cspSource = this._panel.webview.cspSource;
    const suggestionsHtml = suggestions.map((s) => `<div class="card" style="margin-top:10px; border-left:3px solid #007acc; font-size:10px;">${s}</div>`).join("");
    return `<html>
        <head>
            <meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src ${cspSource} https://cdn.jsdelivr.net 'unsafe-inline'; style-src ${cspSource} 'unsafe-inline'; img-src ${cspSource} data:;">
            <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/svg-pan-zoom@3.6.1/dist/svg-pan-zoom.min.js"></script>
            <script>
                const vscode = acquireVsCodeApi();
                let pz = null;

                window.handleNodeClick = function(line) {
                    vscode.postMessage({ command: 'gotoLine', line: line });
                };

                window.addEventListener('message', event => {
                    const message = event.data;
                    if (message.command === 'highlightNodes') {
                        const { nodes, status } = message;
                        const svgElement = document.querySelector('svg');
                        if (!svgElement) return;

                        // Reset previous highlights or apply new ones
                        // In Mermaid, nodes have IDs like 'nLuid_LX' (from our parser)
                        // This logic might need refinement to match step names
                        const allNodes = svgElement.querySelectorAll('.node');
                        allNodes.forEach(node => {
                            const label = node.querySelector('.nodeLabel');
                            if (label) {
                                const text = label.textContent || '';
                                if (nodes.some(n => text.includes(n))) {
                                    if (status === 'error') {
                                        node.style.stroke = '#ff4d4d';
                                        node.style.strokeWidth = '4px';
                                        node.classList.add('node-error');
                                    }
                                }
                            }
                        });
                    }
                });

                async function initMermaid() {
                    const container = document.getElementById('mermaid-container');
                    try {
                        mermaid.initialize({
                            startOnLoad: false,
                            theme: 'base',
                            themeVariables: {
                                primaryColor: '#1e1e1e',
                                primaryTextColor: '#fff',
                                primaryBorderColor: '#007acc',
                                lineColor: '#555',
                                secondaryColor: '#ce9178',
                                tertiaryColor: '#1e1e1e',
                                mainBkg: 'transparent'
                            },
                            securityLevel: 'loose',
                            flowchart: { curve: 'basis', htmlLabels: true }
                        });

                        const { svg } = await mermaid.render('mermaid-svg', \`${graph}\`);
                        container.innerHTML = svg;

                        const svgElement = container.querySelector('svg');
                        if (svgElement) {
                            svgElement.style.width = '100%';
                            svgElement.style.height = '100%';
                            svgElement.style.display = 'block';
                            
                            if (pz) pz.destroy();
                            pz = svgPanZoom(svgElement, {
                                zoomEnabled: true,
                                controlIconsEnabled: false,
                                fit: true,
                                center: true,
                                minZoom: 0.001,
                                maxZoom: 100
                            });

                            document.getElementById('zoom-in').onclick = () => pz.zoomIn();
                            document.getElementById('zoom-out').onclick = () => pz.zoomOut();
                            document.getElementById('zoom-reset').onclick = () => { pz.resetZoom(); pz.center(); };
                            
                            document.getElementById('download-svg').onclick = () => {
                                try {
                                    const serializer = new XMLSerializer();
                                    let source = serializer.serializeToString(svgElement);
                                    source = '<?xml version="1.0" standalone="no"?>\\r\\n' + source;
                                    vscode.postMessage({
                                        command: 'downloadImage',
                                        content: source,
                                        format: 'svg',
                                        fileName: '${fileName.replace(/\.[^/.]+$/, "")}_dag.svg'
                                    });
                                } catch (err) {
                                    console.error('Download error:', err);
                                }
                            };

                            document.getElementById('download-png').onclick = () => {
                                try {
                                    const serializer = new XMLSerializer();
                                    const svgData = serializer.serializeToString(svgElement);
                                    const canvas = document.createElement('canvas');
                                    const ctx = canvas.getContext('2d');
                                    const img = new Image();
                                    const svgBlob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
                                    const url = URL.createObjectURL(svgBlob);

                                    img.onload = () => {
                                        canvas.width = img.width * 2; // High DPI
                                        canvas.height = img.height * 2;
                                        ctx.fillStyle = 'white'; // Background
                                        ctx.fillRect(0, 0, canvas.width, canvas.height);
                                        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                                        URL.revokeObjectURL(url);
                                        const pngData = canvas.toDataURL('image/png');
                                        vscode.postMessage({
                                            command: 'downloadImage',
                                            content: pngData,
                                            format: 'png',
                                            fileName: '${fileName.replace(/\.[^/.]+$/, "")}_dag.png'
                                        });
                                    };
                                    img.src = url;
                                } catch (err) {
                                    console.error('PNG Download error:', err);
                                }
                            };
                        }
                    } catch (e) {
                        container.innerHTML = '<div style="padding:20px; color:#ff4d4d; background:#111; border-radius:8px;">\u274C Mermaid Render Error: ' + e.message + '</div>';
                    }
                }

                window.addEventListener('load', initMermaid);
            </script>
            <style>
                body { background: #0a0a0a; color: #d4d4d4; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 0; overflow: hidden; display: flex; flex-direction: column; height: 100vh; width: 100vw; }
                .glass-header { background: #1a1a1a; padding: 10px 20px; border-bottom: 2px solid #007acc; display: flex; justify-content: space-between; align-items: center; z-index: 1000; flex-shrink: 0; }
                .main-layout { display: flex; flex: 1; overflow: hidden; position: relative; }
                .sidebar { width: 240px; background: #111; border-right: 1px solid #222; padding: 15px; display: flex; flex-direction: column; gap: 15px; z-index: 500; flex-shrink: 0; overflow-y: auto; }
                .canvas { flex: 1; position: relative; background: #000; overflow: hidden; }
                #mermaid-container { position: absolute; top:0; left:0; width: 100%; height: 100%; z-index: 10; display: flex; justify-content: center; align-items: center; background: transparent; }
                .card { background: #1e1e1e; border: 1px solid #333; border-radius: 6px; padding: 12px; }
                .stat-item { display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 6px; }
                .complexity-box { text-align: center; padding: 12px; border-radius: 8px; background: #161616; border-left: 3px solid #ce9178; }
                .footer { background: #111; padding: 5px 20px; border-top: 1px solid #222; font-size: 9px; color: #444; display: flex; justify-content: space-between; flex-shrink: 0; }
                .toolbar { position: absolute; bottom: 20px; right: 20px; display: flex; gap: 5px; background: rgba(30,30,30,0.85); padding: 6px; border-radius: 8px; border: 1px solid #444; z-index: 2000; }
                .toolbar button { background: #444; color: white; border: none; width: 30px; height: 32px; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 16px; transition: 0.2s; }
                .toolbar button:hover { background: #007acc; }
                .btn-primary { width: 100%; padding: 10px; background: #007acc; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 11px; }
                .btn-primary:hover { background: #0098ff; }
                .node-error rect, .node-error circle, .node-error polygon, .node-error path {
                    fill: rgba(255, 77, 77, 0.3) !important;
                    stroke: #ff4d4d !important;
                    stroke-width: 3px !important;
                }
            </style>
        </head>
        <body>
            <header class="glass-header">
                <div><h1 style="margin:0;font-size:15px;font-weight:600;color:#4fc1ff;">\u{1F680} WPipe Analysis Mode</h1></div>
                <div style="text-align:right"><div style="font-size:11px;color:#eee;">${fileName}</div><div style="font-size:8px;color:#555;">Live ${now}</div></div>
            </header>
            <div class="main-layout">
                <aside class="sidebar">
                    <div class="card">
                        <h3 style="margin:0 0 10px 0; font-size:10px; color: #888;">STATS</h3>
                        <div class="stat-item"><span>Steps</span><b>${stats.steps}</b></div>
                        <div class="stat-item"><span>Logic Blocks</span><b>${stats.logic}</b></div>
                        <div class="stat-item"><span>Pipelines</span><b>${stats.pipes}</b></div>
                    </div>
                    <div class="complexity-box">
                        <span style="font-size:8px;color:#666;">COMPUTATIONAL COST</span>
                        <div style="font-size:20px;font-weight:bold;color:#ce9178;margin:2px 0;">${bigO}</div>
                    </div>
                    ${suggestionsHtml}
                    <div style="margin-top:auto; display:flex; flex-direction:column; gap:8px;">
                        <button id="download-svg" class="btn-primary">\u{1F4BE} Download SVG</button>
                        <button id="download-png" class="btn-primary" style="background:#444;">\u{1F5BC}\uFE0F Download PNG</button>
                    </div>
                </aside>
                <main class="canvas">
                    <div id="mermaid-container"></div>
                    <div class="toolbar">
                        <button id="zoom-out" title="Zoom Out">\u2212</button>
                        <button id="zoom-reset" title="Reset Center">\u27F2</button>
                        <button id="zoom-in" title="Zoom In">+</button>
                    </div>
                </main>
            </div>
            <footer class="footer">
                <div>William Rodriguez (wisrovi)</div>
                <div>Engine: <b>Mermaid v10</b></div>
            </footer>
        </body>
        </html>`;
  }
  parse(doc, fileName) {
    const content2 = doc.getText();
    let g = "flowchart TD\n  classDef step fill:#1e1e1e,stroke:#007acc,stroke-width:2px,color:#fff,rx:5,ry:5,cursor:pointer\n  classDef logic fill:#1e1e1e,stroke:#ce9178,stroke-width:2px,color:#fff,rx:2,ry:2,cursor:pointer\n  classDef startN fill:#007acc,stroke:#007acc,color:#fff\n";
    let totalSteps = 0;
    let totalLogic = 0;
    let maxDepth = 0;
    const tree = parser.parse(content2);
    const pipelineInstances = [];
    const addStateCalls = [];
    tree.iterate({
      enter: (node) => {
        if (node.name === "CallExpression") {
          const callText = content2.substring(node.from, node.to);
          if (callText.includes(".set_steps(") || callText.startsWith("Pipeline(") && callText.includes("steps=")) {
            pipelineInstances.push({ text: callText, from: node.from, to: node.to });
          } else if (callText.includes(".add_state(")) {
            addStateCalls.push({ text: callText, from: node.from, to: node.to });
          }
        }
      }
    });
    const seenPipelines = /* @__PURE__ */ new Set();
    pipelineInstances.forEach((inst) => {
      const pipeVar = inst.text.split(".")[0].split("(")[0].trim() || "Pipeline";
      if (seenPipelines.has(pipeVar)) return;
      seenPipelines.add(pipeVar);
      const uid = Math.random().toString(36).substr(2, 5);
      g += `  subgraph sg_${uid} ["\u{1F4E6} ${pipeVar} (in ${fileName})"]
    direction TD
    start_${uid}(( )):::startN
`;
      let stepsContent = "";
      let stepsOffset = inst.from;
      const m1 = inst.text.match(/(?:set_steps|steps)\s*\(\s*\[([\s\S]*?)\]\s*\)/);
      const m2 = inst.text.match(/steps\s*=\s*\[([\s\S]*?)\]/);
      if (m1) {
        stepsContent = m1[1];
        stepsOffset += inst.text.indexOf(m1[1]);
      } else if (m2) {
        stepsContent = m2[1];
        stepsOffset += inst.text.indexOf(m2[1]);
      }
      const res = this.parseRec(doc, stepsContent, stepsOffset, `start_${uid}`, "L" + uid, 0);
      g += res.graph.split("\n").map((l) => l.trim() ? "    " + l : "").join("\n") + "\n";
      totalSteps += res.steps;
      totalLogic += res.logic;
      if (res.depth > maxDepth) maxDepth = res.depth;
      let lastId = res.lastId;
      let lastLabel = res.lastIncomingLabel;
      addStateCalls.forEach((addCall) => {
        if (addCall.text.startsWith(pipeVar + ".add_state(")) {
          const am = addCall.text.match(/\.add_state\s*\(([\s\S]*?)\)/);
          if (am) {
            const amOffset = addCall.from + addCall.text.indexOf(am[1]);
            const res2 = this.parseRec(doc, am[1], amOffset, lastId, "A" + Math.random().toString(36).substr(2, 3), 0, lastLabel);
            g += res2.graph.split("\n").map((l) => l.trim() ? "    " + l : "").join("\n") + "\n";
            totalSteps += res2.steps;
            totalLogic += res2.logic;
            if (res2.depth > maxDepth) maxDepth = res2.depth;
            lastId = res2.lastId;
            lastLabel = res2.lastIncomingLabel;
          }
        }
      });
      g += "  end\n";
    });
    let bigO = "O(n)";
    if (maxDepth === 1) bigO = "O(n\xB2)";
    else if (maxDepth > 1) bigO = `O(n^${maxDepth + 1})`;
    const suggestions = [];
    if (totalSteps > 5 && totalLogic === 0) {
      suggestions.push("\u{1F4A1} Tip: Your pipeline is linear. Consider using 'Parallel' if steps are independent.");
    }
    return {
      graph: seenPipelines.size > 0 ? g : "flowchart TD\n  NoPipe[No pipeline detected]",
      stats: { steps: totalSteps, logic: totalLogic, pipes: seenPipelines.size },
      bigO,
      suggestions
    };
  }
  parseRec(doc, content2, offset, prev, prefix, depth, incomingLabel = "") {
    let graph = "";
    let curr = prev;
    let sCount = 0;
    let lCount = 0;
    let maxSubDepth = depth;
    let currentLabel = incomingLabel;
    const splitWithOffsets2 = (c, baseOffset) => {
      const r = [];
      let cur = "";
      let d = 0;
      let start = 0;
      for (let i = 0; i < c.length; i++) {
        if (c[i] === "[" || c[i] === "(") d++;
        else if (c[i] === "]" || c[i] === ")") d--;
        if (c[i] === "," && d === 0) {
          r.push({ text: cur.trim(), offset: baseOffset + start + (cur.length - cur.trimStart().length) });
          cur = "";
          start = i + 1;
        } else cur += c[i];
      }
      if (cur.trim()) r.push({ text: cur.trim(), offset: baseOffset + start + (cur.length - cur.trimStart().length) });
      return r;
    };
    splitWithOffsets2(content2, offset).forEach((item, i) => {
      const tr = item.text;
      if (!tr) return;
      const line = doc.positionAt(item.offset).line;
      const id2 = "n" + prefix + i + "_L" + line;
      const edge = currentLabel ? `-- ${currentLabel} -->` : "-->";
      currentLabel = "";
      if (tr.startsWith("Condition(")) {
        lCount++;
        const exprMatch = tr.match(/expression\s*=\s*(["'])(.*?)\1/);
        const expr = exprMatch ? exprMatch[2] : "Condition";
        graph += `  ${curr} ${edge} ${id2}{"${expr}"}:::logic
`;
        graph += `  click ${id2} call handleNodeClick("${line}")
`;
        const tCont = this.ext(tr, "branch_true");
        const fCont = this.ext(tr, "branch_false");
        const mid = id2 + "_m";
        if (tCont) {
          const tOffset = item.offset + tr.indexOf(tCont);
          const r = this.parseRec(doc, tCont, tOffset, id2, id2 + "T", depth, "True");
          graph += r.graph + `  ${r.lastId} --> ${mid}(( ))
`;
          sCount += r.steps;
          lCount += r.logic;
          if (r.depth > maxSubDepth) maxSubDepth = r.depth;
        } else graph += `  ${id2} -- True --> ${mid}(( ))
`;
        if (fCont) {
          const fOffset = item.offset + tr.indexOf(fCont);
          const r = this.parseRec(doc, fCont, fOffset, id2, id2 + "F", depth, "False");
          graph += r.graph + `  ${r.lastId} --> ${mid}(( ))
`;
          sCount += r.steps;
          lCount += r.logic;
          if (r.depth > maxSubDepth) maxSubDepth = r.depth;
        } else graph += `  ${id2} -- False --> ${mid}(( ))
`;
        curr = mid;
      } else if (tr.startsWith("Parallel(")) {
        lCount++;
        graph += `  ${curr} ${edge} ${id2}[[" \u26A1 Parallel "]]:::logic
`;
        graph += `  click ${id2} call handleNodeClick("${line}")
`;
        const pCont = this.ext(tr, "steps");
        const mid = id2 + "_m";
        if (pCont) {
          const pOffset = item.offset + tr.indexOf(pCont);
          this.smartSplitWithOffsets(pCont, pOffset).forEach((ps, pi) => {
            const r = this.parseRec(doc, ps.text, ps.offset, id2, id2 + "P" + pi, depth, "flow");
            graph += r.graph + `  ${r.lastId} --> ${mid}(( ))
`;
            sCount += r.steps;
            lCount += r.logic;
            if (r.depth > maxSubDepth) maxSubDepth = r.depth;
          });
        } else {
          graph += `  ${id2} --> ${mid}(( ))
`;
        }
        curr = mid;
      } else if (tr.startsWith("For(")) {
        lCount++;
        graph += `  ${curr} ${edge} ${id2}[[" \u{1F504} For Loop "]]:::logic
`;
        graph += `  click ${id2} call handleNodeClick("${line}")
`;
        const fCont = this.ext(tr, "steps");
        if (fCont) {
          const fOffset = item.offset + tr.indexOf(fCont);
          const r = this.parseRec(doc, fCont, fOffset, id2, id2 + "F", depth + 1, "body");
          graph += r.graph + `  ${r.lastId} --> ${id2}
`;
          sCount += r.steps;
          lCount += r.logic;
          if (r.depth > maxSubDepth) maxSubDepth = r.depth;
        }
        curr = id2;
        currentLabel = "exit";
      } else if (tr.startsWith("Background(")) {
        lCount++;
        const lblMatch = tr.match(/Background\((.*?)\)/);
        const lbl = lblMatch ? lblMatch[1].split(",")[0].trim() : "BG Task";
        graph += `  ${curr} -. async .-> ${id2}((" \u26A1 ${lbl} ")):::step
`;
        graph += `  click ${id2} call handleNodeClick("${line}")
`;
      } else {
        let lbl = tr.split("(")[0].replace(/[\[\]]/g, "").trim();
        if (lbl) {
          sCount++;
          graph += `  ${curr} ${edge} ${id2}[" \u{1F680} ${lbl} "]:::step
`;
          graph += `  click ${id2} call handleNodeClick("${line}")
`;
          curr = id2;
        }
      }
    });
    return { graph, lastId: curr, steps: sCount, logic: lCount, depth: maxSubDepth, lastIncomingLabel: currentLabel };
  }
  smartSplitWithOffsets(c, baseOffset) {
    const r = [];
    let cur = "";
    let d = 0;
    let start = 0;
    for (let i = 0; i < c.length; i++) {
      if (c[i] === "[" || c[i] === "(") d++;
      else if (c[i] === "]" || c[i] === ")") d--;
      if (c[i] === "," && d === 0) {
        r.push({ text: cur.trim(), offset: baseOffset + start + (cur.length - cur.trimStart().length) });
        cur = "";
        start = i + 1;
      } else cur += c[i];
    }
    if (cur.trim()) r.push({ text: cur.trim(), offset: baseOffset + start + (cur.length - cur.trimStart().length) });
    return r;
  }
  ext(c, a) {
    const m = c.match(new RegExp(`${a}\\s*=\\s*\\[`));
    if (m) {
      let s = m.index + m[0].length;
      let d = 1;
      for (let i = s; i < c.length; i++) {
        if (c[i] === "[") d++;
        else if (c[i] === "]") d--;
        if (d === 0) return c.substring(s, i);
      }
    }
    return null;
  }
  smartSplit(c) {
    const r = [];
    let cur = "";
    let d = 0;
    for (let i = 0; i < c.length; i++) {
      if (c[i] === "[" || c[i] === "(") d++;
      else if (c[i] === "]" || c[i] === ")") d--;
      if (c[i] === "," && d === 0) {
        r.push(cur.trim());
        cur = "";
      } else cur += c[i];
    }
    if (cur.trim()) r.push(cur.trim());
    return r;
  }
};

// src/webviews/cheatSheet.ts
var vscode6 = __toESM(require("vscode"));
function showCheatSheet() {
  const panel = vscode6.window.createWebviewPanel("wpipeCheatSheet", "\u{1F680} WPipe Professional Cheat Sheet", vscode6.ViewColumn.Beside, { enableScripts: true });
  panel.webview.html = `
        <html>
        <head>
            <style>
                :root {
                    --bg: #0d1117;
                    --card-bg: #161b22;
                    --border: #30363d;
                    --text: #c9d1d9;
                    --accent: #58a6ff;
                    --secondary: #7ee787;
                    --orange: #ffa657;
                    --code-bg: #000;
                }
                body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; padding: 0; margin: 0; background: var(--bg); color: var(--text); }
                .container { max-width: 1000px; margin: 0 auto; padding: 40px 20px; }
                header { border-bottom: 1px solid var(--border); padding-bottom: 20px; margin-bottom: 40px; display: flex; align-items: center; justify-content: space-between; }
                h1 { font-size: 28px; margin: 0; color: var(--accent); display: flex; align-items: center; gap: 10px; }
                h2 { font-size: 20px; color: var(--secondary); margin-top: 30px; border-left: 4px solid var(--secondary); padding-left: 10px; }
                h3 { font-size: 16px; color: var(--orange); margin-top: 20px; }
                .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
                .card { background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; padding: 20px; transition: transform 0.2s; }
                .card:hover { border-color: var(--accent); }
                code { background: var(--code-bg); padding: 2px 6px; border-radius: 4px; font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; font-size: 13px; color: var(--orange); }
                .snippet-list { list-style: none; padding: 0; }
                .snippet-list li { margin-bottom: 15px; border-bottom: 1px solid #21262d; padding-bottom: 10px; }
                .snippet-name { font-weight: bold; color: var(--accent); font-size: 14px; }
                .snippet-desc { font-size: 12px; color: #8b949e; margin-top: 4px; }
                .command-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
                .command-table td { padding: 10px; border-bottom: 1px solid var(--border); font-size: 13px; }
                .command-table .cmd { color: var(--secondary); font-weight: bold; }
                .footer { margin-top: 60px; text-align: center; font-size: 12px; color: #8b949e; border-top: 1px solid var(--border); padding-top: 20px; }
                .badge { display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: bold; text-transform: uppercase; background: #238636; color: white; margin-left: 5px; }
                .warning-box { background: rgba(255, 166, 87, 0.1); border-left: 4px solid var(--orange); padding: 15px; margin: 20px 0; border-radius: 4px; font-size: 13px; }
            </style>
        </head>
        <body>
            <div class="container">
                <header>
                    <h1>\u{1F680} WPipe Tools <span style="font-size:14px; color:#8b949e; font-weight:normal;">v0.8.2 Professional Edition</span></h1>
                    <div style="font-size: 12px; color: var(--accent);">By William Rodriguez (wisrovi)</div>
                </header>

                <div class="warning-box">
                    <b>\u{1F4A1} Pro Tip:</b> Always initialize your <code>Pipeline</code> with a <code>tracking_db</code> to enable forensic error capture, event logging, and real-time dashboard monitoring.
                </div>

                <h2>\u{1F6E0}\uFE0F Commands & Automation</h2>
                <div class="grid">
                    <div class="card">
                        <h3>Visual Analysis</h3>
                        <table class="command-table">
                            <tr><td class="cmd">Preview DAG</td><td>Watch your architecture come to life. Refreshes on save.</td></tr>
                            <tr><td class="cmd">Dashboard</td><td>Launch the real-time web monitoring interface.</td></tr>
                        </table>
                    </div>
                    <div class="card">
                        <h3>Step Management</h3>
                        <table class="command-table">
                            <tr><td class="cmd">Cloud Catalog</td><td>Search & import 130+ community steps instantly.</td></tr>
                            <tr><td class="cmd">Run Step</td><td>Test individual <code>@step</code> functions without running the whole pipe.</td></tr>
                        </table>
                    </div>
                </div>

                <h2>\u{1F40D} Python Snippets (Speed Up Development)</h2>
                <div class="grid">
                    <div class="card">
                        <h3>\u2728 Core Components</h3>
                        <ul class="snippet-list">
                            <li><span class="snippet-name">wpstep</span> <span class="badge">Common</span><div class="snippet-desc">Function-based step. Best for simple logic.</div></li>
                            <li><span class="snippet-name">wpstate</span><div class="snippet-desc">Class-based step with typed <code>PipelineContext</code>.</div></li>
                            <li><span class="snippet-name">wpstepadv</span> <span class="badge">Enterprise</span><div class="snippet-desc">Professional class with retries, timeouts, and rich metadata.</div></li>
                        </ul>
                    </div>
                    <div class="card">
                        <h3>\u{1F300} Flow Control</h3>
                        <ul class="snippet-list">
                            <li><span class="snippet-name">wpparallel</span><div class="snippet-desc">Execute multiple steps simultaneously with thread management.</div></li>
                            <li><span class="snippet-name">wpcondition</span><div class="snippet-desc">Boolean branching (True/False) based on data content.</div></li>
                            <li><span class="snippet-name">wpfor</span><div class="snippet-desc">Iterative loops with early exit validation.</div></li>
                            <li><span class="snippet-name">wpbackground</span><div class="snippet-desc">Fire-and-forget asynchronous execution.</div></li>
                        </ul>
                    </div>
                    <div class="card">
                        <h3>\u{1F3D7}\uFE0F Orchestration</h3>
                        <ul class="snippet-list">
                            <li><span class="snippet-name">wppipe</span><div class="snippet-desc">Basic pipeline skeleton with error handling.</div></li>
                            <li><span class="snippet-name">wppipeadv</span> <span class="badge">LTS</span><div class="snippet-desc">Full production setup: Metrics, Resource Monitor, Task Timer.</div></li>
                            <li><span class="snippet-name">wperrorcapture</span><div class="snippet-desc">Custom global error handler for forensic analysis.</div></li>
                        </ul>
                    </div>
                    <div class="card">
                        <h3>\u{1F6E1}\uFE0F Resilience & Tracking</h3>
                        <ul class="snippet-list">
                            <li><span class="snippet-name">wpevent</span><div class="snippet-desc">Log custom markers in the execution timeline.</div></li>
                            <li><span class="snippet-name">wpalert</span><div class="snippet-desc">Set thresholds (CPU, RAM, Time) to trigger alerts.</div></li>
                            <li><span class="snippet-name">wpcheckpoint</span><div class="snippet-desc">Save points for resumable long-running pipelines.</div></li>
                        </ul>
                    </div>
                </div>

                <h2>\u{1F4DC} YAML Configuration</h2>
                <div class="grid">
                    <div class="card">
                        <h3>Structure</h3>
                        <ul class="snippet-list">
                            <li><span class="snippet-name">wpyaml</span><div class="snippet-desc">Main pipeline YAML header.</div></li>
                            <li><span class="snippet-name">ypstep</span><div class="snippet-desc">Standard task definition in config files.</div></li>
                        </ul>
                    </div>
                    <div class="card">
                        <h3>Blocks</h3>
                        <ul class="snippet-list">
                            <li><span class="snippet-name">ypparallel / ypcondition</span><div class="snippet-desc">Logic blocks for data-driven configuration.</div></li>
                            <li><span class="snippet-name">ypfor / ypbackground</span><div class="snippet-desc">Advanced flow control in YAML.</div></li>
                        </ul>
                    </div>
                </div>

                <div class="footer">
                    Engineered for excellence in data orchestration.<br/>
                    Copyright &copy; 2026 WPipe Tools | <a href="https://github.com/wisrovi/wpipe" style="color:var(--accent);">Official Docs</a>
                </div>
            </div>
        </body>
        </html>
    `;
}

// src/webviews/aiAssistant.ts
var vscode7 = __toESM(require("vscode"));
function showAiAssistant(extensionUri) {
  const panel = vscode7.window.createWebviewPanel(
    "wpipeAI",
    "WPipe AI Assistant",
    vscode7.ViewColumn.Beside,
    {
      enableScripts: true,
      retainContextWhenHidden: true
    }
  );
  panel.webview.html = getHtml(panel.webview);
  panel.webview.onDidReceiveMessage((message) => {
    if (message.command === "generate") {
      const prompt = message.text.toLowerCase();
      let code = "";
      if (prompt.includes("download") && prompt.includes("sqlite")) {
        code = `from wpipe import Pipeline, step, SQLiteTracking

@step(name="fetch_data")
def fetch_data():
    return {"data": "..."}

@step(name="save_to_db")
def save_to_db(context):
    # logic to save
    pass

pipe = Pipeline(name="AI Generated Pipeline", tracking_db=SQLiteTracking("data.db"))
pipe.set_steps([fetch_data, save_to_db])
pipe.run()`;
      } else if (prompt.includes("parallel")) {
        code = `from wpipe import Pipeline, step, Parallel

@step(name="task_1")
def task_1(): pass

@step(name="task_2")
def task_2(): pass

pipe = Pipeline(name="Parallel Pipeline")
pipe.set_steps([
    Parallel(steps=[task_1, task_2])
])
pipe.run()`;
      } else {
        code = `# AI suggest: Try asking for "download and sqlite" or "parallel pipeline"
@step(name="my_step")
def my_step():
    pass`;
      }
      panel.webview.postMessage({ command: "result", code });
    } else if (message.command === "insert") {
      const editor = vscode7.window.activeTextEditor;
      if (editor) {
        editor.edit((eb) => {
          eb.insert(editor.selection.active, message.code);
        });
      }
    }
  });
}
function getHtml(webview) {
  return `<!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: sans-serif; padding: 20px; background: #1e1e1e; color: #ccc; }
            input { width: 100%; padding: 10px; background: #333; color: white; border: 1px solid #444; border-radius: 4px; margin-bottom: 10px; }
            button { background: #007acc; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
            pre { background: #000; padding: 15px; border-radius: 4px; overflow-x: auto; color: #9cdcfe; border: 1px solid #333; }
            .chat-msg { margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <h2>\u{1F916} WPipe AI Assistant</h2>
        <div class="chat-msg">
            <p>Describe what you want to build:</p>
            <input type="text" id="prompt" placeholder="e.g. A pipeline with parallel tasks...">
            <button onclick="generate()">Generate Structure</button>
        </div>
        <div id="output" style="display:none;">
            <h3>Generated Code:</h3>
            <pre id="code-block"></pre>
            <button onclick="insert()">Insert into Editor</button>
        </div>
        <script>
            const vscode = acquireVsCodeApi();
            function generate() {
                const text = document.getElementById('prompt').value;
                vscode.postMessage({ command: 'generate', text: text });
            }
            function insert() {
                const code = document.getElementById('code-block').innerText;
                vscode.postMessage({ command: 'insert', code: code });
            }
            window.addEventListener('message', event => {
                const message = event.data;
                if (message.command === 'result') {
                    document.getElementById('output').style.display = 'block';
                    document.getElementById('code-block').innerText = message.code;
                }
            });
        </script>
    </body>
    </html>`;
}

// src/commands/dashboard.ts
var vscode9 = __toESM(require("vscode"));

// src/webviews/dashboardPanel.ts
var vscode8 = __toESM(require("vscode"));
var DashboardPanel = class _DashboardPanel {
  constructor(panel, port) {
    this._disposables = [];
    this._panel = panel;
    this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
    this._update(port);
  }
  static createOrShow(extensionUri, port) {
    const column = vscode8.window.activeTextEditor ? vscode8.window.activeTextEditor.viewColumn : void 0;
    if (_DashboardPanel.currentPanel) {
      _DashboardPanel.currentPanel._panel.reveal(column);
      _DashboardPanel.currentPanel._update(port);
      return;
    }
    const panel = vscode8.window.createWebviewPanel(
      "wpipeDashboard",
      "WPipe Dashboard",
      column || vscode8.ViewColumn.One,
      {
        enableScripts: true,
        retainContextWhenHidden: true
      }
    );
    _DashboardPanel.currentPanel = new _DashboardPanel(panel, port);
  }
  dispose() {
    _DashboardPanel.currentPanel = void 0;
    this._panel.dispose();
    while (this._disposables.length) {
      const x = this._disposables.pop();
      if (x) {
        x.dispose();
      }
    }
  }
  _update(port) {
    this._panel.title = `WPipe Dashboard (Port ${port})`;
    this._panel.webview.html = this._getHtmlForWebview(port);
  }
  _getHtmlForWebview(port) {
    const url = `http://localhost:${port}`;
    return `<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>WPipe Dashboard</title>
            <style>
                body, html {
                    margin: 0;
                    padding: 0;
                    height: 100%;
                    width: 100%;
                    overflow: hidden;
                    background-color: #1e1e1e;
                }
                iframe {
                    border: none;
                    width: 100%;
                    height: 100%;
                    background-color: #fff;
                }
                .loading-container {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    color: #ccc;
                    font-family: sans-serif;
                    z-index: -1;
                }
            </style>
        </head>
        <body>
            <div class="loading-container">
                Connecting to WPipe Dashboard on port ${port}...
            </div>
            <iframe src="${url}" allow="autoplay; clipboard-read; clipboard-write;"></iframe>
            <script>
                // Handle potential connection issues or iframe loading
                const iframe = document.querySelector('iframe');
                iframe.onload = () => {
                    console.log('Dashboard iframe loaded');
                };
            </script>
        </body>
        </html>`;
  }
};

// src/commands/dashboard.ts
async function openDashboard(context, dbPath) {
  console.log("\u{1F680} WPipe: openDashboard called with:", dbPath);
  if (vscode9.env.uiKind === vscode9.UIKind.Web) {
    vscode9.window.showErrorMessage("WPipe Dashboard requires a local Python environment.");
    return;
  }
  let finalDbPath;
  let potentialDbPath = "";
  if (typeof dbPath === "string" && dbPath.length > 0) {
    potentialDbPath = dbPath;
  } else if (dbPath && typeof dbPath === "object" && "fsPath" in dbPath) {
    potentialDbPath = dbPath.fsPath;
  }
  if (potentialDbPath && (potentialDbPath.endsWith(".db") || potentialDbPath.endsWith(".sqlite") || potentialDbPath.endsWith(".sqlite3"))) {
    finalDbPath = potentialDbPath;
  }
  if (!finalDbPath) {
    const dbUri = await vscode9.window.showOpenDialog({
      canSelectFiles: true,
      canSelectFolders: false,
      canSelectMany: false,
      filters: { "Database": ["db", "sqlite", "sqlite3"], "All Files": ["*"] },
      title: "Select WPipe Tracking Database"
    });
    if (!dbUri) return;
    finalDbPath = dbUri[0].fsPath;
  }
  const useConfig = await vscode9.window.showQuickPick(["No", "Yes"], { placeHolder: "Select WPipe Config Directory? (Optional)" });
  let configPath = "";
  if (useConfig === "Yes") {
    const configUri = await vscode9.window.showOpenDialog({
      canSelectFiles: false,
      canSelectFolders: true,
      canSelectMany: false,
      title: "Select WPipe Config Directory"
    });
    if (configUri) configPath = configUri[0].fsPath;
  }
  const port = await vscode9.window.showInputBox({
    placeHolder: "5000",
    prompt: "Enter port for the dashboard",
    value: "5000"
  }) || "5000";
  const terminal = vscode9.window.createTerminal("WPipe Dashboard");
  let cmd = `wpipe dashboard --db "${finalDbPath}" --port ${port}`;
  if (configPath) cmd += ` --config-dir "${configPath}"`;
  terminal.show();
  terminal.sendText(cmd);
  vscode9.window.showInformationMessage(`\u{1F680} Starting WPipe Dashboard inside VS Code...`);
  setTimeout(() => {
    DashboardPanel.createOrShow(context.extensionUri, port);
  }, 2500);
}

// src/commands/replayLogs.ts
var vscode10 = __toESM(require("vscode"));
var fs = __toESM(require("fs"));
var errorDecorationType = vscode10.window.createTextEditorDecorationType({
  backgroundColor: "rgba(255, 0, 0, 0.2)",
  isWholeLine: true,
  overviewRulerColor: "red",
  overviewRulerLane: vscode10.OverviewRulerLane.Full,
  after: {
    contentText: " \u26A0\uFE0F WPipe Error",
    color: "red",
    margin: "0 0 0 1em"
  }
});
async function replayLogErrors() {
  const logUri = await vscode10.window.showOpenDialog({
    canSelectFiles: true,
    canSelectFolders: false,
    canSelectMany: false,
    filters: { "Log Files": ["log"] },
    title: "Select WPipe Log File"
  });
  if (!logUri || logUri.length === 0) return;
  const logPath = logUri[0].fsPath;
  const content2 = fs.readFileSync(logPath, "utf8");
  const lines = content2.split("\n");
  const errors = [];
  const logPattern = /^.*? \| (ERROR|CRITICAL) \| (.*?):(.*?):(\d+) \| (.*)$/;
  for (const line of lines) {
    const match = line.match(logPattern);
    if (match) {
      errors.push({
        level: match[1],
        module: match[2],
        function: match[3],
        line: parseInt(match[4]) - 1,
        // 0-indexed for VS Code
        message: match[5]
      });
    }
  }
  if (errors.length === 0) {
    vscode10.window.showInformationMessage("\u2705 No errors found in the selected log.");
    return;
  }
  vscode10.window.showWarningMessage(`\u{1F50D} Found ${errors.length} errors in log. Highlighting in editor...`);
  for (const error of errors) {
    const files = await vscode10.workspace.findFiles(`**/${error.module}.py`);
    if (files.length > 0) {
      const doc = await vscode10.workspace.openTextDocument(files[0]);
      const editor = await vscode10.window.showTextDocument(doc, { preview: false });
      const decoration = {
        range: new vscode10.Range(error.line, 0, error.line, 0),
        hoverMessage: `**[WPipe ${error.level}]** ${error.message}`
      };
      editor.setDecorations(errorDecorationType, [decoration]);
      if (error === errors[0]) {
        editor.revealRange(decoration.range, vscode10.TextEditorRevealType.InCenter);
      }
    }
  }
  if (DAGPanel.currentPanel) {
    const stepNames = errors.map((e) => e.function);
    DAGPanel.currentPanel.highlightNodes(stepNames, "error");
  }
}

// src/commands/impactAnalysis.ts
var vscode11 = __toESM(require("vscode"));
var path2 = __toESM(require("path"));
async function findStepUsage(arg) {
  let stepName;
  if (typeof arg === "string") {
    stepName = arg;
  } else if (arg instanceof vscode11.TreeItem) {
    stepName = arg.label;
  }
  if (!stepName) {
    stepName = await vscode11.window.showInputBox({
      prompt: "Enter the name of the step to analyze impact",
      placeHolder: "e.g. download_data"
    });
  }
  if (!stepName) return;
  await vscode11.window.withProgress({
    location: vscode11.ProgressLocation.Notification,
    title: `Analyzing impact for step: ${stepName}`,
    cancellable: false
  }, async (progress) => {
    const files = await vscode11.workspace.findFiles("**/*.py", "**/node_modules/**");
    const usages = [];
    for (const file of files) {
      const doc = await vscode11.workspace.openTextDocument(file);
      const content2 = doc.getText();
      const lines = content2.split("\n");
      lines.forEach((line, index) => {
        const regex = new RegExp(`\\b${stepName}\\b`);
        if (regex.test(line)) {
          if (!line.includes(`def ${stepName}`) && !line.includes(`@step`)) {
            usages.push({ file, line: index, text: line.trim() });
          }
        }
      });
    }
    if (usages.length === 0) {
      vscode11.window.showInformationMessage(`\u2705 Step '${stepName}' is not used in any other pipeline.`);
      return;
    }
    const items = usages.map((u) => ({
      label: `${path2.basename(u.file.fsPath)}:L${u.line + 1}`,
      description: u.text,
      uri: u.file,
      line: u.line
    }));
    const selected = await vscode11.window.showQuickPick(items, {
      placeHolder: `Found ${usages.length} usages of '${stepName}'. Select to open.`
    });
    if (selected) {
      const doc = await vscode11.workspace.openTextDocument(selected.uri);
      const editor = await vscode11.window.showTextDocument(doc);
      const pos = new vscode11.Position(selected.line, 0);
      editor.selection = new vscode11.Selection(pos, pos);
      editor.revealRange(new vscode11.Range(pos, pos), vscode11.TextEditorRevealType.InCenter);
    }
  });
}

// src/providers/codeLensProvider.ts
var vscode12 = __toESM(require("vscode"));
var path3 = __toESM(require("path"));
var WPipeCodeLensProvider = class {
  async provideCodeLenses(document, token) {
    const lenses = [];
    const content2 = document.getText();
    try {
      const tree = parser.parse(content2);
      tree.iterate({
        enter: (node) => {
          if (node.name === "Decorator") {
            const decText = content2.substring(node.from, node.to);
            if (decText.startsWith("@step")) {
              const range = new vscode12.Range(
                document.positionAt(node.from),
                document.positionAt(node.to)
              );
              lenses.push(new vscode12.CodeLens(range, {
                title: "$(play) Run Step",
                command: "wpipeSteps.runStepFromCode",
                arguments: [document.fileName, range.start.line]
              }));
            }
          } else if (node.name === "CallExpression") {
            const callText = content2.substring(node.from, node.to);
            if (callText.includes("Pipeline(") || callText.includes(".run(")) {
              const range = new vscode12.Range(
                document.positionAt(node.from),
                document.positionAt(node.to)
              );
              lenses.push(new vscode12.CodeLens(range, {
                title: "$(play) Run Pipeline",
                command: "wpipe-vscode.runPipeline",
                arguments: [document.fileName]
              }));
              lenses.push(new vscode12.CodeLens(range, {
                title: "$(graph) Preview DAG",
                command: "wpipe-vscode.previewDAG"
              }));
              const dbMatch = callText.match(/tracking_db\s*=\s*['"](.*?)['"]/);
              if (dbMatch) {
                const relativeDbPath = dbMatch[1];
                let absoluteDbPath = relativeDbPath;
                if (!path3.isAbsolute(relativeDbPath)) {
                  const workspaceFolder = vscode12.workspace.getWorkspaceFolder(document.uri);
                  if (workspaceFolder) {
                    absoluteDbPath = path3.join(workspaceFolder.uri.fsPath, relativeDbPath);
                  }
                }
                lenses.push(new vscode12.CodeLens(range, {
                  title: "$(dashboard) Open Dashboard",
                  command: "wpipe-vscode.openDashboard",
                  arguments: [absoluteDbPath]
                }));
              }
            }
            if (callText.includes(".set_steps(")) {
              const range = new vscode12.Range(
                document.positionAt(node.from),
                document.positionAt(node.to)
              );
              lenses.push(new vscode12.CodeLens(range, {
                title: "$(plus) Add Logic Block",
                command: "wpipe-vscode.addLogicBlock",
                arguments: [range]
              }));
            }
          }
        }
      });
    } catch (e) {
    }
    return lenses;
  }
};

// src/providers/hoverProvider.ts
var vscode13 = __toESM(require("vscode"));
var WPipeHoverProvider = class {
  provideHover(document, position) {
    const range = document.getWordRangeAtPosition(position);
    if (!range) return null;
    const word = document.getText(range);
    const wsStep = WorkspaceIndex.getStep(word);
    if (wsStep) {
      const md = new vscode13.MarkdownString();
      md.appendMarkdown(`### \u{1F680} WPipe Step: ${wsStep.name}
`);
      md.appendMarkdown(`**Version:** ${wsStep.version}

`);
      if (wsStep.description) md.appendMarkdown(`**Description:** ${wsStep.description}

`);
      md.appendMarkdown(`---
*Location:* ${vscode13.workspace.asRelativePath(wsStep.filePath)}:${wsStep.line + 1}`);
      return new vscode13.Hover(md);
    }
    const catStep = CatalogManager.getSteps().find((s) => s.name === word || s.func_name === word);
    if (catStep) {
      const md = new vscode13.MarkdownString();
      md.appendMarkdown(`### \u{1F4E6} WPipe Library: ${catStep.name}
`);
      md.appendMarkdown(`**Module:** \`${catStep.namespace}\`

`);
      md.appendMarkdown(`**Author:** ${catStep.author || "Official"}
`);
      md.appendMarkdown(`**Repo:** ${catStep.repo}

`);
      md.appendMarkdown(`---
Click to insert import and usage.`);
      return new vscode13.Hover(md);
    }
    return null;
  }
};

// src/providers/codeActionProvider.ts
var vscode14 = __toESM(require("vscode"));
var WPipeCodeActionProvider = class {
  static {
    this.providedCodeActionKinds = [
      vscode14.CodeActionKind.QuickFix
    ];
  }
  provideCodeActions(document, range, context, token) {
    const actions = [];
    const content2 = document.getText();
    try {
      const tree = parser.parse(content2);
      tree.iterate({
        enter: (node) => {
          if (node.name === "FunctionDefinition") {
            const funcRange = new vscode14.Range(
              document.positionAt(node.from),
              document.positionAt(node.to)
            );
            if (range.intersection(funcRange)) {
              let hasStepDecorator = false;
              let parent = node.node.parent;
              if (parent) {
                parent.getChildren("Decorator").forEach((dec) => {
                  const decText = content2.substring(dec.from, dec.to);
                  if (decText.startsWith("@step")) {
                    hasStepDecorator = true;
                  }
                });
              }
              if (!hasStepDecorator) {
                const action = new vscode14.CodeAction("Convert to WPipe Step", vscode14.CodeActionKind.QuickFix);
                action.edit = new vscode14.WorkspaceEdit();
                const nameNode = node.node.getChild("VariableName");
                const funcName = nameNode ? content2.substring(nameNode.from, nameNode.to) : "my_step";
                const decorator = `@step(name="${funcName}", version="1.0.0")
`;
                action.edit.insert(document.uri, document.positionAt(node.from), decorator);
                if (!content2.includes("from wpipe import step")) {
                  action.edit.insert(document.uri, new vscode14.Position(0, 0), "from wpipe import step\n");
                }
                actions.push(action);
              }
            }
          }
        }
      });
    } catch (e) {
    }
    return actions;
  }
};

// src/core/diagnostics.ts
var vscode15 = __toESM(require("vscode"));
function registerDiagnostics(context) {
  const diagnosticCollection = vscode15.languages.createDiagnosticCollection("wpipe");
  context.subscriptions.push(diagnosticCollection);
  if (vscode15.window.activeTextEditor) {
    updateDiagnostics(vscode15.window.activeTextEditor.document, diagnosticCollection);
  }
  context.subscriptions.push(
    vscode15.workspace.onDidChangeTextDocument((e) => updateDiagnostics(e.document, diagnosticCollection)),
    vscode15.window.onDidChangeActiveTextEditor((editor) => {
      if (editor) updateDiagnostics(editor.document, diagnosticCollection);
    })
  );
}
function updateDiagnostics(document, collection) {
  if (document.languageId !== "python") return;
  const diagnostics = [];
  const content2 = document.getText();
  const tree = parser.parse(content2);
  const workspaceSteps = new Set(WorkspaceIndex.getAllSteps().map((s) => s.name));
  const catalogSteps = new Set(CatalogManager.getSteps().map((s) => s.name));
  const knownSteps = /* @__PURE__ */ new Set([...workspaceSteps, ...catalogSteps]);
  tree.iterate({
    enter: (node) => {
      if (node.name === "CallExpression") {
        const callText = content2.substring(node.from, node.to);
        if (callText.includes(".set_steps(") || callText.includes("Pipeline(") && callText.includes("steps=")) {
          const match = callText.match(/(?:set_steps|steps)\s*\(\s*\[([\s\S]*?)\]\s*\)/) || callText.match(/steps\s*=\s*\[([\s\S]*?)\]/);
          if (match) {
            const stepsContent = match[1];
            const baseOffset = node.from + callText.indexOf(match[1]);
            const parts = splitWithOffsets(stepsContent, baseOffset);
            parts.forEach((part) => {
              const name2 = part.text.split("(")[0].trim();
              const logicBlocks = ["Condition", "Parallel", "For", "Background"];
              if (name2 && !logicBlocks.includes(name2) && !knownSteps.has(name2)) {
                const range = new vscode15.Range(
                  document.positionAt(part.offset),
                  document.positionAt(part.offset + name2.length)
                );
                diagnostics.push(new vscode15.Diagnostic(
                  range,
                  `Step '${name2}' not found in workspace or catalog.`,
                  vscode15.DiagnosticSeverity.Warning
                ));
              }
            });
          }
        }
      }
    }
  });
  collection.set(document.uri, diagnostics);
}
function splitWithOffsets(c, baseOffset) {
  const r = [];
  let cur = "";
  let d = 0;
  let start = 0;
  for (let i = 0; i < c.length; i++) {
    if (c[i] === "[" || c[i] === "(") d++;
    else if (c[i] === "]" || c[i] === ")") d--;
    if (c[i] === "," && d === 0) {
      r.push({ text: cur.trim(), offset: baseOffset + start + (cur.length - cur.trimStart().length) });
      cur = "";
      start = i + 1;
    } else cur += c[i];
  }
  if (cur.trim()) r.push({ text: cur.trim(), offset: baseOffset + start + (cur.length - cur.trimStart().length) });
  return r;
}

// src/wizards/stepWizard.ts
var vscode16 = __toESM(require("vscode"));
var path4 = __toESM(require("path"));
async function createNewStepWizard() {
  const workspaceFolders = vscode16.workspace.workspaceFolders;
  if (!workspaceFolders) {
    vscode16.window.showErrorMessage("Please open a workspace before creating a new step.");
    return;
  }
  const rootPath = workspaceFolders[0].uri.fsPath;
  const statesPath = path4.join(rootPath, "states");
  const stepName = await vscode16.window.showInputBox({
    prompt: "Enter the name of the new step (e.g. DataProcessor)",
    placeHolder: "MyNewStep",
    validateInput: (value) => {
      if (!value) return "Step name is required";
      if (!/^[A-Za-z][A-Za-z0-9_]*$/.test(value)) return "Invalid Python identifier";
      return null;
    }
  });
  if (!stepName) return;
  const formattedStepName = stepName.split(/[_-]/).map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join("");
  const fileName = stepName.replace(/([a-z])([A-Z])/g, "$1_$2").toLowerCase() + ".py";
  const filePath = path4.join(statesPath, fileName);
  const template = `from wpipe import step, to_obj
from wpipe.timeout import timeout_sync
from typing import Any
from pydantic import BaseModel

class ${formattedStepName}Context(BaseModel):
    field: str

@step(
    name="${formattedStepName}",
    version="v1.0",
    timeout=10,
    description="Description of the step ${formattedStepName}",
    tags=["custom"],
    retry_count=3,
    retry_delay=0.01,
)
class ${formattedStepName}:
    """
    Advanced WPipe State: ${formattedStepName}
    Generated by WPipe Tools Wizard.
    """
    
    def __init__(self, config: str = "value"):
        self.config = config

    @timeout_sync(seconds=2)
    @to_obj(${formattedStepName}Context)
    def __call__(self, context: Any) -> Any:
        # Professional logic here
        print(f"\u{1F680} Executing ${formattedStepName} with config: {self.config}")
        return context
`;
  try {
    const statesUri = vscode16.Uri.file(statesPath);
    await vscode16.workspace.fs.createDirectory(statesUri);
    const initUri = vscode16.Uri.joinPath(statesUri, "__init__.py");
    let initContent = "";
    try {
      const existingInit = await vscode16.workspace.fs.readFile(initUri);
      initContent = new TextDecoder().decode(existingInit);
    } catch {
    }
    const importLine = `from .${fileName.replace(".py", "")} import ${formattedStepName}
`;
    if (!initContent.includes(importLine)) {
      initContent += importLine;
      await vscode16.workspace.fs.writeFile(initUri, new TextEncoder().encode(initContent));
    }
    const fileUri = vscode16.Uri.file(filePath);
    await vscode16.workspace.fs.writeFile(fileUri, new TextEncoder().encode(template));
    const doc = await vscode16.workspace.openTextDocument(fileUri);
    await vscode16.window.showTextDocument(doc);
    vscode16.window.showInformationMessage(`\u2705 Step '${formattedStepName}' created successfully in states/${fileName}`);
  } catch (err) {
    vscode16.window.showErrorMessage(`\u274C Failed to create step: ${err.message}`);
  }
}

// src/extension.ts
var path5 = __toESM(require("path"));
async function activate(context) {
  console.log("\u{1F680} WPipe Tools: Activation started...");
  CatalogManager.init(context);
  WorkspaceIndex.indexWorkspace();
  registerDiagnostics(context);
  const stepProvider = new WPipeStepProvider();
  vscode17.window.registerTreeDataProvider("wpipeSteps", stepProvider);
  context.subscriptions.push(
    vscode17.languages.registerCodeLensProvider({ language: "python" }, new WPipeCodeLensProvider()),
    vscode17.languages.registerHoverProvider({ language: "python" }, new WPipeHoverProvider()),
    vscode17.languages.registerCodeActionsProvider({ language: "python" }, new WPipeCodeActionProvider(), {
      providedCodeActionKinds: WPipeCodeActionProvider.providedCodeActionKinds
    })
  );
  context.subscriptions.push(
    vscode17.commands.registerCommand("wpipeSteps.refreshEntry", () => stepProvider.refresh()),
    vscode17.commands.registerCommand("wpipe-vscode.refreshCatalog", () => CatalogManager.update(context, true)),
    vscode17.commands.registerCommand("wpipe-vscode.createNewStep", createNewStepWizard),
    vscode17.commands.registerCommand("wpipeSteps.openFile", async (f, l) => {
      const doc = await vscode17.workspace.openTextDocument(vscode17.Uri.file(f));
      const editor = await vscode17.window.showTextDocument(doc);
      const p = new vscode17.Position(l, 0);
      editor.selection = new vscode17.Selection(p, p);
      editor.revealRange(new vscode17.Range(p, p), vscode17.TextEditorRevealType.InCenter);
    }),
    vscode17.commands.registerCommand("wpipeSteps.insertStep", (step) => {
      const editor = vscode17.window.activeTextEditor;
      if (editor) {
        editor.edit((eb) => {
          const importCode = `from ${step.namespace} import ${step.func_name}
`;
          eb.insert(new vscode17.Position(0, 0), importCode);
          const isClass = /^[A-Z]/.test(step.func_name);
          eb.insert(editor.selection.active, isClass ? `${step.func_name}(),` : `${step.func_name},`);
        });
        vscode17.window.showInformationMessage(`\u2705 Estado '${step.name}' insertado con \xE9xito.`);
      }
    }),
    vscode17.commands.registerCommand("wpipe-vscode.searchSteps", async () => {
      const items = CatalogManager.getSteps().map((s) => ({
        label: `$(rocket) ${s.name}`,
        description: `${s.repo} | Author: ${s.author || "Official"}`,
        detail: `Module: ${s.namespace}`,
        step: s
      }));
      const sel = await vscode17.window.showQuickPick(items, { placeHolder: "Buscar estado en el cat\xE1logo oficial o comunidad..." });
      if (sel) {
        vscode17.commands.executeCommand("wpipeSteps.insertStep", sel.step);
      }
    }),
    vscode17.commands.registerCommand("wpipe-vscode.previewDAG", () => {
      const editor = vscode17.window.activeTextEditor;
      if (editor) DAGPanel.createOrShow(context.extensionUri, editor.document);
    }),
    vscode17.commands.registerCommand("wpipe-vscode.openDashboard", (dbPath) => openDashboard(context, dbPath)),
    vscode17.commands.registerCommand("wpipe-vscode.replayLogs", replayLogErrors),
    vscode17.commands.registerCommand("wpipe-vscode.findStepUsage", (stepName) => findStepUsage(stepName)),
    vscode17.commands.registerCommand("wpipe-vscode.showCheatSheet", showCheatSheet),
    vscode17.commands.registerCommand("wpipe-vscode.openAiAssistant", () => showAiAssistant(context.extensionUri)),
    vscode17.commands.registerCommand("wpipe-vscode.runPipeline", async (filePath) => {
      if (vscode17.env.uiKind === vscode17.UIKind.Web) {
        vscode17.window.showErrorMessage("Running pipelines requires a local Python environment.");
        return;
      }
      const terminal = vscode17.window.createTerminal(`Pipeline: ${path5.basename(filePath)}`);
      terminal.show();
      terminal.sendText(`python "${filePath}"`);
    }),
    vscode17.commands.registerCommand("wpipe-vscode.addLogicBlock", async (range) => {
      const editor = vscode17.window.activeTextEditor;
      if (!editor) return;
      const text = editor.document.getText(range);
      const openBracketIndex = text.indexOf("[");
      if (openBracketIndex !== -1) {
        const offset = editor.document.offsetAt(range.start) + openBracketIndex + 1;
        const pos = editor.document.positionAt(offset);
        editor.selection = new vscode17.Selection(pos, pos);
      }
      const items = [
        {
          label: "$(split-horizontal) Condition",
          detail: "Boolean branching (True/False)",
          snippet: 'Condition(\n    expression="${1:valor > 100}",\n    branch_true=[${2:step_true}],\n    branch_false=[${3:step_false}]\n)'
        },
        {
          label: "$(sync) For Loop",
          detail: "Iterative loop with validation",
          snippet: "For(\n    iterations=${1:10},\n    validation_expression=\"${2:status != 'error'}\",\n    steps=[${3:step_to_repeat}]\n)"
        },
        {
          label: "$(zap) Parallel",
          detail: "Concurrent multi-step execution",
          snippet: "Parallel(\n    steps=[${1:step1}, ${2:step2}],\n    max_workers=${3:2}\n)"
        },
        {
          label: "$(run-all) Background",
          detail: "Asynchronous fire-and-forget task",
          snippet: "Background(${1:slow_step})"
        }
      ];
      const sel = await vscode17.window.showQuickPick(items, { placeHolder: "Select a logic block to insert inside set_steps..." });
      if (sel) {
        editor.insertSnippet(new vscode17.SnippetString(sel.snippet));
      }
    }),
    vscode17.commands.registerCommand("wpipeSteps.runStep", async (item) => {
      if (vscode17.env.uiKind === vscode17.UIKind.Web) {
        vscode17.window.showErrorMessage("Running steps requires a local Python environment.");
        return;
      }
      if (!item || !item.filePath) return;
      const terminal = vscode17.window.createTerminal(`Run Step: ${item.label}`);
      terminal.show();
      terminal.sendText(`python "${item.filePath}"`);
    }),
    vscode17.commands.registerCommand("wpipeSteps.runStepFromCode", async (filePath, line) => {
      if (vscode17.env.uiKind === vscode17.UIKind.Web) {
        vscode17.window.showErrorMessage("Running steps requires a local Python environment.");
        return;
      }
      const fileName = path5.basename(filePath);
      const terminal = vscode17.window.createTerminal(`Run Step: ${fileName}`);
      terminal.show();
      terminal.sendText(`python "${filePath}"`);
    }),
    vscode17.commands.registerCommand("wpipeSteps.installRequirements", async (item) => {
      if (vscode17.env.uiKind === vscode17.UIKind.Web) {
        vscode17.window.showErrorMessage("Installing requirements requires a local environment.");
        return;
      }
      if (!item || !item.step || !item.step.requirements) {
        vscode17.window.showWarningMessage("Este paso no tiene requerimientos externos definidos.");
        return;
      }
      const reqUrl = item.step.requirements;
      const terminal = vscode17.window.createTerminal(`Install: ${item.step.name}`);
      terminal.show();
      try {
        const response = await fetch(reqUrl);
        if (!response.ok) throw new Error(`No se pudo descargar el archivo: ${response.statusText}`);
        const content2 = await response.text();
        let tempReqUri;
        const workspaceFolders = vscode17.workspace.workspaceFolders;
        if (workspaceFolders && workspaceFolders.length > 0) {
          tempReqUri = vscode17.Uri.joinPath(workspaceFolders[0].uri, `requirements_${item.step.name}.txt`);
        } else {
          await vscode17.workspace.fs.createDirectory(context.globalStorageUri);
          tempReqUri = vscode17.Uri.joinPath(context.globalStorageUri, `requirements_${item.step.name}.txt`);
        }
        await vscode17.workspace.fs.writeFile(tempReqUri, new TextEncoder().encode(content2));
        terminal.sendText(`pip install -r "${tempReqUri.fsPath}"`);
        vscode17.window.showInformationMessage(`\u23F3 Descargado e instalando dependencias para '${item.step.name}'...`);
      } catch (error) {
        vscode17.window.showErrorMessage(`\u274C Error al preparar requerimientos: ${error}`);
      }
    }),
    vscode17.commands.registerCommand("wpipeSteps.viewExamples", async (item) => {
      if (!item || !item.step || !item.step.examples) {
        vscode17.window.showWarningMessage("Este paso no tiene ejemplos configurados.");
        return;
      }
      let uiUrl = item.step.examples.replace("raw.githubusercontent.com", "github.com");
      const parts = uiUrl.split("/");
      if (parts.length >= 6) {
        const owner = parts[3];
        const repo = parts[4];
        const branch = parts[5];
        const rest = parts.slice(6).join("/");
        const type = item.step.examples.endsWith("/") ? "tree" : "blob";
        uiUrl = `https://github.com/${owner}/${repo}/${type}/${branch}/${rest}`;
      }
      vscode17.env.openExternal(vscode17.Uri.parse(uiUrl));
    }),
    vscode17.commands.registerCommand("wpipeSteps.downloadExample", async (item) => {
      if (!item || !item.step || !item.step.examples) {
        vscode17.window.showWarningMessage("Este paso no tiene ejemplos configurados.");
        return;
      }
      let rawUrl = item.step.examples;
      try {
        if (rawUrl.endsWith("/")) {
          const parts = rawUrl.split("/");
          const owner = parts[3];
          const repo = parts[4];
          const branch = parts[5];
          const pathInRepo = parts.slice(6).join("/");
          const apiUrl = `https://api.github.com/repos/${owner}/${repo}/contents/${pathInRepo}?ref=${branch}`;
          const apiResponse = await fetch(apiUrl);
          if (!apiResponse.ok) throw new Error(`No se pudo listar el contenido de la carpeta: ${apiResponse.statusText}`);
          const files = await apiResponse.json();
          if (!Array.isArray(files)) throw new Error("Respuesta inesperada de la API de GitHub.");
          const pyFiles = files.filter((f) => f.name.endsWith(".py")).map((f) => ({
            label: `$(file-code) ${f.name}`,
            url: f.download_url,
            name: f.name
          }));
          if (pyFiles.length === 0) {
            vscode17.window.showInformationMessage("No se encontraron archivos de ejemplo (.py) en la carpeta.");
            return;
          }
          const selected = await vscode17.window.showQuickPick(pyFiles, {
            placeHolder: "Selecciona un ejemplo para usar como plantilla:"
          });
          if (!selected) return;
          rawUrl = selected.url;
        }
        await vscode17.window.withProgress({
          location: vscode17.ProgressLocation.Notification,
          title: `Descargando plantilla...`,
          cancellable: false
        }, async () => {
          const response = await fetch(rawUrl);
          if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);
          const content2 = await response.text();
          if (content2.trim().startsWith("<!DOCTYPE html>")) {
            throw new Error("La URL no apunta a un archivo RAW v\xE1lido.");
          }
          const doc = await vscode17.workspace.openTextDocument({
            content: content2,
            language: "python"
          });
          await vscode17.window.showTextDocument(doc);
          vscode17.window.showInformationMessage(`\u2705 Plantilla cargada con \xE9xito.`);
        });
      } catch (error) {
        vscode17.window.showErrorMessage(`\u274C Fallo al procesar plantilla: ${error}`);
      }
    })
  );
}
function deactivate() {
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  activate,
  deactivate
});
