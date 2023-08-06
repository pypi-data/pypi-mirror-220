from copy import deepcopy
from collections import defaultdict
import logging
from smatchpp import util
from smatchpp import interfaces
from smatchpp import subgraph_extraction

logger = logging.getLogger("__main__")

def rmquote(triple):
    """remove quotes froms string"""
    
    f = lambda x: x.replace("\"", "").replace("'", "")
    
    triple = (f(triple[0]), f(triple[1]), f(triple[2]))

    return triple


class AMRGraphStandardizer(interfaces.GraphStandardizer):
    """Class for graph standardization

       This class allows standardization of amr graphs, i.a., 
       node/edge reification, quote removal, etc.

       Attributes:
           reify_nodes (bool): reify nodes, e.g. (x, polarity, -) 
                                -> (x, polarity, z), (z, instance, -)
           reify_edges (bool): reify edges e.g, (x, location, y) 
                                -> (z, instance, locatedAt), (z, a1, x), (z, a2, y)
           dereify_edges (bool): inverse of edge reification
           lower (bool): lower case, e.g. (x, op1, "Obama") -> (x, op1, "obama")
           reomve_quotes (bool): remove quotes e.g. (x, op1, "Obama") -> (x, op1, Obama)
           deinvert_edges (bool): deinvert edges, e.g. (x,a-of,y) -> (y, a, x)
           norm_logical_ops (bool): or and and will be treated as commutative, e.g.,
                                    (x, instance, and), (x, op1, y), (x, op2, z)
                                    -> (x, instance, and), (x, op, y), (x, op, z)
           use_concept_as_root (bool): do smatch style, where root is not attached to
                                        a var, but concept to var via root relation 
                                        (xvar, :root, concept) if false, we use (xvar, :root, root_of_graph)
    """


    def __init__(self, reify_nodes=False, edges=None, lower=True, 
                 relabel_vars=True, remove_quote=True, 
                 deinvert_edges=True, norm_logical_ops=False, 
                 use_concept_as_root=True, remove_duplicates=True,
                 semantic_standardization=False):

        self.lower = lower
        self.relabel_vars = relabel_vars
        self.reify_nodes = reify_nodes
        self.edges = edges
        self._maybe_set_reify_rules()
        
        self.deinvert_edges = deinvert_edges
        self.remove_quote = remove_quote
        self.norm_logical_ops = norm_logical_ops
        self.use_concept_as_root = use_concept_as_root
        self.remove_duplicates = remove_duplicates
        self.semantic_standardization = semantic_standardization
        self._maybe_prepare_semantic_standardization()

        return None

    def _standardize(self, triples):
        """Triple standardization according to parameters specified in init"""

        triples = deepcopy(triples)
        logging.debug("standardizing triples") 
        logging.debug("1. input: {}".format(triples)) 
        
        if self.lower:
            triples = [(s.lower(), r.lower(), t.lower()) for (s, r, t) in triples]
            logging.debug("2. lower cased: {}".format(triples)) 
        if self.relabel_vars:
            self._relabel_vars(triples)
            logging.debug("3. ensure no varname qual concept: {}".format(triples)) 
        if self.reify_nodes:
            self._reify_n(triples)
            logging.debug("4. reify nodes: {}".format(triples)) 
        if self.deinvert_edges:
            self._deinvert_e(triples)
            logging.debug("5. deinvert edges: {}".format(triples)) 
        if self.edges == "reify":
            self._reify_e(triples)
            logging.debug("6. edge reififcation: {}".format(triples)) 
        if self.edges == "dereify":
            self._dereify_e(triples)
            logging.debug("7. edge dereififcation: {}".format(triples)) 
        if self.norm_logical_ops:
            self._norm_logical_ops(triples)
            logging.debug("8. norm logical operators: {}".format(triples)) 
        if self.remove_quote:
            triples = [rmquote(t) for t in triples]
            logging.debug("9. remove quotes: {}".format(triples)) 
        if self.use_concept_as_root:
            self._concept_as_root(triples)
            logging.debug("10. make concept to root (smatch style): {}".format(triples)) 
        if self.remove_duplicates:
            triples = list(set(triples))
            logging.debug("11. removed duplicate triples: {}".format(triples)) 
        if self.semantic_standardization:
            triples = subgraph_extraction.semantically_standardize_graph(triples, 
                                                                            self.inverted_frame_table, 
                                                                            self.amr_aspects)
            logging.debug("12. semantically standardized triples: {}".format(triples)) 
        return triples

    def _maybe_prepare_semantic_standardization(self):
        if self.semantic_standardization:
            self.amr_aspects = util.read_amr_aspects()
            frame_table = util.read_frame_table()
            self.inverted_frame_table = util.invert_frame_table(frame_table, self.amr_aspects)
        return None

    def _relabel_vars(self, triples):
        """standardize variable names"""
        
        v2c = util.get_var_concept_dict(triples)
        constants = util.get_constant_set(triples)

        # standardize and make variable names simpler "(xyds / cat)" -> "(c / cat)"
        # just for optics and better alignment interpretation
        v2v = {}
        vnew_idx = {}
        for v in v2c:
            concept = v2c[v]
            vnew = concept[0]
            if vnew not in vnew_idx:
                v2v[v] = vnew
                vnew_idx[vnew] = 1
            else:
                v2v[v] = vnew + str(vnew_idx[vnew])
                vnew_idx[vnew] += 1
        
        # take care that there are no variable names that are same as concepts
        # some parsers and the reference does this, can lead to bugs
        # so we will change "(i / i)" -> "(ix / i)"
        for v in v2v:
            vnew = v2v[v]
            while vnew in constants:
                vnew += "x"
            v2v[v] = vnew

        # now we can map to new variables
        for i in range(len(triples)):
            src = triples[i][0]
            rel = triples[i][1]
            tgt = triples[i][2]
            if src in v2v:
                src = v2v[src]
            if tgt in v2v:
                if rel != ":instance":
                    tgt = v2v[tgt]
            triples[i] = (src, triples[i][1], tgt)
        
        return None

    def _concept_as_root(self, triples):
        vc = util.get_var_concept_dict(triples)
        for i, tr in enumerate(triples):
            if tr[1] == ":root":
                newtriple = (tr[2], ":root", vc[tr[2]])
                triples[i] = newtriple
        return None

    def _maybe_set_reify_rules(self):
        self.reify_rules, self.reify_rules_inverse = {}, {}
        if self.edges:
            self.reify_rules, self.reify_rules_inverse = util.read_reify_table(lower=self.lower)
        return None

    def _reify_n(self, triples):
        """Reify constant nodes.
            
           constant nodes are targets with no outgoing edge (leaves) 
           that don't have an incoming :instance edge.

           E.g., (x, :polarity, -) ---> (x, :polarity, y), (y, :instance, -)
        """

        collect_ids = set()
        for i, tr in enumerate(triples):
            target = tr[2]
            incoming_instance = False
            for tr2 in triples:
                if tr2[1] == ":instance" and tr2[0] == target:
                    incoming_instance = True
                if tr2[1] == ":instance" and tr2[2] == target:
                    incoming_instance = True
            if not incoming_instance:
                collect_ids.add(i)
        newvarkey = "rfattribute_"
        idx = 0
        for cid in collect_ids:
            varname = newvarkey + str(idx)
            triples.append((triples[cid][0], triples[cid][1], varname))
            triples.append((varname, ":instance", triples[cid][2]))
            idx += 1
        for i in reversed(sorted(list(collect_ids))):
            del triples[i]
        return None

    def _deinvert_e(self, triples):
        
        for i in range(len(triples)):
            s, r, t = triples[i]
            r = r.split("-of")
            if len(r) > 1:
                r = r[0]
                triples[i] = (t, r, s)
        
        return None

    def _reify_e(self, triples):
        """Reify edges accoding to rules"""

        new = []
        delis = []
        for i, tr in enumerate(triples):
            rel = tr[1]
            if rel in self.reify_rules:
                new.append(("ric" + str(i), ":instance", self.reify_rules[rel][0]))
                new.append(("ric" + str(i), self.reify_rules[rel][1], tr[0]))
                new.append(("ric" + str(i), self.reify_rules[rel][2], tr[2]))
                delis.append(i)
        for index in sorted(delis, reverse=True):
            del triples[index]    
        triples += new
        return None
        
    def _maybe_get_dereification(self, variable, triples):
        
        concept = None
        for i, tr in enumerate(triples):
            if tr[0] == variable and tr[1] == ":instance":
                concept = tr[2]
                ci = i
                break
        if concept not in self.reify_rules_inverse:
            return False
        
        for tr in triples:
            if tr[2] == variable:
                return False
        
        foundx = 0
        foundxv = None
        foundxi = None
        foundy = 0
        foundyv = None
        foundyi = None
        foundother = 0
        
        for i, tr in enumerate(triples):
            if tr[0] == variable and tr[1] != ":instance":
                if tr[1] == self.reify_rules_inverse[concept][1]:
                    foundx += 1
                    foundxv = tr[2]
                    foundxi = i
                elif tr[1] == self.reify_rules_inverse[concept][2]:
                    foundy += 1
                    foundyv = tr[2] 
                    foundyi = i
                else:
                    foundother += 1
        
        if foundx == foundy == 1 and foundother == 0:
            return (foundxv, foundyv, foundxi, foundyi, ci, self.reify_rules_inverse[concept][0])
        
        return False

    
    def _dereify_e(self, triples):
        """De-reify edges according to rules"""

        new = []
        delis = []
        done = []
        incoming_map = {}
        for i, tr in enumerate(triples):
            var = tr[0]
            if var in done or util.isroot(var, triples):
                continue
            rule = self._maybe_get_dereification(var, triples)
            done.append(var)
            if not rule:
                continue
            src, tgt, deli1, deli2, deli3, rel = rule
            delis.append(deli1)
            delis.append(deli2)
            delis.append(deli3)
            new.append((src, rel, tgt))
            incoming_map[var] = src
        for index in sorted(delis, reverse=True):
            del triples[index] 
        for i, tr in enumerate(triples):
            src = tr[0]
            rel = tr[1]
            tgt = tr[2]
            if tgt in incoming_map:
                tgt = incoming_map[tgt]
                triples[i] = (src, rel, tgt)
        
        triples += new
        
        return None
    
    @staticmethod
    def _norm_logical_ops(triples):
        """Norm logical operators
           
           E.g. (x, :instance, and), (x, :op1, y), (x, :op2, z)
                ---> (x, :instance, and), (x, :op, y), (x, :op, z)
        """

        rel_from_op = []
        for i in range(len(triples)):
            s, r, t = triples[i]
            if ":op" in r:
                for j in range(len(triples)):
                    sx, rx, tx = triples[j]
                    if sx == s and rx == ":instance" and tx in ["or", "and"]:
                        rel_from_op.append(i)
        for i in range(len(triples)):
            if i in rel_from_op:
                s, r, t = triples[i]
                r = ":op"
                triples[i] = (s, r, t)
        return None
        

class AMRGraphPairPreparer(interfaces.GraphPairPreparer):
    """Class for prepairing graph pairs

       Some standardization may involve a graph pair, e.g., 
       when we simplify coreference in two graphs

       Attributes:
            method (str): either "basic" or "reduced". If reduced, we apply content reduction
                          via coreference simplification
            rename_vars (bool): we rename variables in two graphs
    """

    def __init__(self, lossless_graph_compression=False, rename_vars=True):

        self.lossless_graph_compression = lossless_graph_compression
        self.rename_vars = rename_vars

    def _prepare_get_vars(self, triples1, triples2):
        
        logger.debug("preparing graph pair...")
        triples1, triples2 = deepcopy(triples1), deepcopy(triples2)
        var1 = None
        var2 = None
        if self.lossless_graph_compression:    
            logger.debug("lossless content conversion input graph 1: {}".format(triples1))
            logger.debug("lossless content conversion input graph 2: {}".format(triples2))
            var1, var2 = self._transform(triples1, triples2)
            logger.debug("lossless content conversion output graph 1: {}".format(triples1))
            logger.debug("lossless content conversion output graph 2: {}".format(triples2))
        
        else:
            var1 = util.get_var_concept_dict(triples1)
            var2 = util.get_var_concept_dict(triples2)
            var1 = var1.keys()
            var2 = var2.keys()
         
        var1 = set(var1)
        var2 = set(var2)
        #var1.remove("root_of_graph")
        #var2.remove("root_of_graph")
            
        logger.debug("varset graph 1: {}".format(var1))
        logger.debug("varset graph 2: {}".format(var2))
        
        if self.rename_vars:
            logger.debug("renaming vars in graph 1...")
            var_newvar = {v: "aa_" + v for v in var1}
            for i in range(len(triples1)):
                src = triples1[i][0]
                tgt = triples1[i][2]
                if src in var_newvar:
                    src = var_newvar[src]
                if tgt in var_newvar and not triples1[i][1] == ":instance":
                    tgt = var_newvar[tgt]
                triples1[i] = (src, triples1[i][1], tgt)
            var1 = var_newvar.values()
            var1 = set(var1)
            logger.debug("renamed vars graph 1: {}".format(var1))
            logger.debug("new graph 1: {}".format(triples1))
            
            logger.debug("renaming vars in graph 2...")
            var_newvar = {v: "bb_" + v for v in var2}

            for i in range(len(triples2)):
                src = triples2[i][0]
                tgt = triples2[i][2]
                if src in var_newvar:
                    src = var_newvar[src]
                if tgt in var_newvar and not triples2[i][1] == ":instance":
                    tgt = var_newvar[tgt]
                triples2[i] = (src, triples2[i][1], tgt)
            
            var2 = var_newvar.values()
            var2 = set(var2)
            
            logger.debug("renamed vars graph 2: {}".format(var2))
            logger.debug("new graph 2: {}".format(triples2))
        #triples1 = list(sorted(triples1))
        #triples2 = list(sorted(triples2))
        return triples1, triples2, var1, var2
    
    @staticmethod
    def _transform_with_dict(triples, single_ref, var_concept):
        delis = []
        for i, tr in enumerate(triples):
            src = tr[0]
            rel = tr[1]
            tgt = tr[2]
            concepts = var_concept.get(src)
            if concepts in single_ref:
                src = var_concept[src]
            if rel not in [":instance", ":root"] and var_concept.get(tgt) in single_ref:
                tgt = var_concept[tgt]
            if concepts in single_ref and rel == ":instance":
                delis.append(i)
            triples[i] = (src, rel, tgt)
        for index in sorted(delis, reverse=True):
            del triples[index] 
        return None

    def _transform(self, triples1, triples2):

        var_concept1 = util.get_var_concept_dict(triples1)
        var_concept2 = util.get_var_concept_dict(triples2)
        concept_count1 = defaultdict(int)
        concept_count2 = defaultdict(int)
        
        for _, c in var_concept1.items():
            concept_count1[c] += 1 
        for _, c in var_concept2.items():
            concept_count2[c] += 1 
        
        single_ref = set()
        for c in set(concept_count1.keys()).union(set(concept_count2.keys())):
            co1 = concept_count1[c]
            co2 = concept_count2[c]
            if co1 + co2 == 1:
                single_ref.add(c)
            elif co1 == co2 == 1:
                single_ref.add(c)
        
        self._transform_with_dict(triples1, single_ref, var_concept1)
        self._transform_with_dict(triples2, single_ref, var_concept2)

        vc1 = util.get_var_concept_dict(triples1)
        vc2 = util.get_var_concept_dict(triples2)

        return vc1.keys(), vc2.keys()
                
 
