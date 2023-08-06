from __future__ import annotations
from typing import overload, Any, List, Dict, Tuple, Set, Sequence, Union
from pyopenms import *  # pylint: disable=wildcard-import; lgtm(py/polluting-import)
import numpy as _np

from enum import Enum as _PyEnum


def __static_IonIdentityMolecularNetworking_annotateConsensusMap(consensus_map: ConsensusMap ) -> None:
    """
    Cython signature: void annotateConsensusMap(ConsensusMap & consensus_map)
        Annotate ConsensusMap for ion identity molecular networking (IIMN) workflow by GNPS.
        
        Adds meta values Constants::UserParams::IIMN_ROW_ID (unique index for each feature), Constants::UserParams::IIMN_ADDUCT_PARTNERS (related features row IDs)
        and Constants::UserParams::IIMN_ANNOTATION_NETWORK_NUMBER (all related features with different adduct states) get the same network number).
        This method requires the features annotated with the Constants::UserParams::IIMN_LINKED_GROUPS meta value.
        If at least one of the features has an annotation for Constants::UserParam::IIMN_LINKED_GROUPS, annotate ConsensusMap for IIMN.
        
        
        :param consensus_map: Input ConsensusMap without IIMN annotations.
    """
    ...

def __static_MRMRTNormalizer_chauvenet(residuals: List[float] , pos: int ) -> bool:
    """
    Cython signature: bool chauvenet(libcpp_vector[double] residuals, int pos)
    """
    ...

def __static_MRMRTNormalizer_chauvenet_probability(residuals: List[float] , pos: int ) -> float:
    """
    Cython signature: double chauvenet_probability(libcpp_vector[double] residuals, int pos)
    """
    ...

def __static_MRMRTNormalizer_computeBinnedCoverage(rtRange: List[float, float] , pairs: List[List[float, float]] , nrBins: int , minPeptidesPerBin: int , minBinsFilled: int ) -> bool:
    """
    Cython signature: bool computeBinnedCoverage(libcpp_pair[double,double] rtRange, libcpp_vector[libcpp_pair[double,double]] & pairs, int nrBins, int minPeptidesPerBin, int minBinsFilled)
    """
    ...

def __static_FeatureFinderAlgorithmIsotopeWavelet_getProductName() -> Union[bytes, str, String]:
    """
    Cython signature: String getProductName()
    """
    ...

def __static_MRMRTNormalizer_removeOutliersIterative(pairs: List[List[float, float]] , rsq_limit: float , coverage_limit: float , use_chauvenet: bool , outlier_detection_method: bytes ) -> List[List[float, float]]:
    """
    Cython signature: libcpp_vector[libcpp_pair[double,double]] removeOutliersIterative(libcpp_vector[libcpp_pair[double,double]] & pairs, double rsq_limit, double coverage_limit, bool use_chauvenet, libcpp_string outlier_detection_method)
    """
    ...

def __static_MRMRTNormalizer_removeOutliersRANSAC(pairs: List[List[float, float]] , rsq_limit: float , coverage_limit: float , max_iterations: int , max_rt_threshold: float , sampling_size: int ) -> List[List[float, float]]:
    """
    Cython signature: libcpp_vector[libcpp_pair[double,double]] removeOutliersRANSAC(libcpp_vector[libcpp_pair[double,double]] & pairs, double rsq_limit, double coverage_limit, size_t max_iterations, double max_rt_threshold, size_t sampling_size)
    """
    ...

def __static_IonIdentityMolecularNetworking_writeSupplementaryPairTable(consensus_map: ConsensusMap , output_file: Union[bytes, str, String] ) -> None:
    """
    Cython signature: void writeSupplementaryPairTable(const ConsensusMap & consensus_map, const String & output_file)
        Write supplementary pair table (csv file) from a ConsensusMap with edge annotations for connected features. Required for GNPS IIMN.
        
        The table contains the columns "ID 1" (row ID of first feature), "ID 2" (row ID of second feature), "EdgeType" (MS1/2 annotation),
        "Score" (the number of direct partners from both connected features) and "Annotation" (adducts and delta m/z between two connected features).
        
        
        :param consensus_map: Input ConsensusMap annotated with IonIdentityMolecularNetworking.annotateConsensusMap.
        :param output_file: Output file path for the supplementary pair table.
    """
    ...


class Acquisition:
    """
    Cython implementation of _Acquisition

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Acquisition.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Acquisition()
        """
        ...
    
    @overload
    def __init__(self, in_0: Acquisition ) -> None:
        """
        Cython signature: void Acquisition(Acquisition &)
        """
        ...
    
    def getIdentifier(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getIdentifier()
        """
        ...
    
    def setIdentifier(self, identifier: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setIdentifier(const String & identifier)
        """
        ...
    
    def isMetaEmpty(self) -> bool:
        """
        Cython signature: bool isMetaEmpty()
        Returns if the MetaInfo is empty
        """
        ...
    
    def clearMetaInfo(self) -> None:
        """
        Cython signature: void clearMetaInfo()
        Removes all meta values
        """
        ...
    
    def metaRegistry(self) -> MetaInfoRegistry:
        """
        Cython signature: MetaInfoRegistry metaRegistry()
        Returns a reference to the MetaInfoRegistry
        """
        ...
    
    def getKeys(self, keys: List[bytes] ) -> None:
        """
        Cython signature: void getKeys(libcpp_vector[String] & keys)
        Fills the given vector with a list of all keys for which a value is set
        """
        ...
    
    def getMetaValue(self, in_0: Union[bytes, str, String] ) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getMetaValue(String)
        Returns the value corresponding to a string, or
        """
        ...
    
    def setMetaValue(self, in_0: Union[bytes, str, String] , in_1: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setMetaValue(String, DataValue)
        Sets the DataValue corresponding to a name
        """
        ...
    
    def metaValueExists(self, in_0: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool metaValueExists(String)
        Returns whether an entry with the given name exists
        """
        ...
    
    def removeMetaValue(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void removeMetaValue(String)
        Removes the DataValue corresponding to `name` if it exists
        """
        ...
    
    def __richcmp__(self, other: Acquisition, op: int) -> Any:
        ... 


class AnnotationStatistics:
    """
    Cython implementation of _AnnotationStatistics

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AnnotationStatistics.html>`_
    """
    
    states: List[int]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AnnotationStatistics()
        """
        ...
    
    @overload
    def __init__(self, in_0: AnnotationStatistics ) -> None:
        """
        Cython signature: void AnnotationStatistics(AnnotationStatistics &)
        """
        ...
    
    def __richcmp__(self, other: AnnotationStatistics, op: int) -> Any:
        ... 


class Base64:
    """
    Cython implementation of _Base64

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Base64.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Base64()
        Class to encode and decode Base64, it supports two precisions 32 bit (float) and 64 bit (double).
        """
        ...
    
    @overload
    def __init__(self, in_0: Base64 ) -> None:
        """
        Cython signature: void Base64(Base64 &)
        """
        ...
    
    def encodeIntegers(self, in_: List[int] , to_byte_order: int , out: String , zlib_compression: bool ) -> None:
        """
        Cython signature: void encodeIntegers(libcpp_vector[int] & in_, ByteOrder to_byte_order, String & out, bool zlib_compression)
        Encodes a vector of integer point numbers to a Base64 string
        """
        ...
    
    def decodeIntegers(self, in_: Union[bytes, str, String] , from_byte_order: int , out: List[int] , zlib_compression: bool ) -> None:
        """
        Cython signature: void decodeIntegers(const String & in_, ByteOrder from_byte_order, libcpp_vector[int] & out, bool zlib_compression)
        Decodes a Base64 string to a vector of integer numbers
        """
        ...
    
    def encodeStrings(self, in_: List[bytes] , out: String , zlib_compression: bool ) -> None:
        """
        Cython signature: void encodeStrings(libcpp_vector[String] & in_, String & out, bool zlib_compression)
        Encodes a vector of strings to a Base64 string
        """
        ...
    
    def decodeStrings(self, in_: Union[bytes, str, String] , out: List[bytes] , zlib_compression: bool ) -> None:
        """
        Cython signature: void decodeStrings(const String & in_, libcpp_vector[String] & out, bool zlib_compression)
        Decodes a Base64 string to a vector of (null-terminated) strings
        """
        ...
    ByteOrder : __ByteOrder 


class CVMappingTerm:
    """
    Cython implementation of _CVMappingTerm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CVMappingTerm.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CVMappingTerm()
        """
        ...
    
    @overload
    def __init__(self, in_0: CVMappingTerm ) -> None:
        """
        Cython signature: void CVMappingTerm(CVMappingTerm &)
        """
        ...
    
    def setAccession(self, accession: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setAccession(String accession)
        Sets the accession string of the term
        """
        ...
    
    def getAccession(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getAccession()
        Returns the accession string of the term
        """
        ...
    
    def setUseTermName(self, use_term_name: bool ) -> None:
        """
        Cython signature: void setUseTermName(bool use_term_name)
        Sets whether the term name should be used, instead of the accession
        """
        ...
    
    def getUseTermName(self) -> bool:
        """
        Cython signature: bool getUseTermName()
        Returns whether the term name should be used, instead of the accession
        """
        ...
    
    def setUseTerm(self, use_term: bool ) -> None:
        """
        Cython signature: void setUseTerm(bool use_term)
        Sets whether the term itself can be used (or only its children)
        """
        ...
    
    def getUseTerm(self) -> bool:
        """
        Cython signature: bool getUseTerm()
        Returns true if the term can be used, false if only children are allowed
        """
        ...
    
    def setTermName(self, term_name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setTermName(String term_name)
        Sets the name of the term
        """
        ...
    
    def getTermName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getTermName()
        Returns the name of the term
        """
        ...
    
    def setIsRepeatable(self, is_repeatable: bool ) -> None:
        """
        Cython signature: void setIsRepeatable(bool is_repeatable)
        Sets whether this term can be repeated
        """
        ...
    
    def getIsRepeatable(self) -> bool:
        """
        Cython signature: bool getIsRepeatable()
        Returns true if this term can be repeated, false otherwise
        """
        ...
    
    def setAllowChildren(self, allow_children: bool ) -> None:
        """
        Cython signature: void setAllowChildren(bool allow_children)
        Sets whether children of this term are allowed
        """
        ...
    
    def getAllowChildren(self) -> bool:
        """
        Cython signature: bool getAllowChildren()
        Returns true if the children of this term are allowed to be used
        """
        ...
    
    def setCVIdentifierRef(self, cv_identifier_ref: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCVIdentifierRef(String cv_identifier_ref)
        Sets the CV identifier reference string, e.g. UO for unit obo
        """
        ...
    
    def getCVIdentifierRef(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCVIdentifierRef()
        Returns the CV identifier reference string
        """
        ...
    
    def __richcmp__(self, other: CVMappingTerm, op: int) -> Any:
        ... 


class ChannelInfo:
    """
    Cython implementation of _ChannelInfo

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ChannelInfo.html>`_
    """
    
    description: bytes
    
    name: int
    
    id: int
    
    center: float
    
    active: bool 


class ChromatogramExtractor:
    """
    Cython implementation of _ChromatogramExtractor

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ChromatogramExtractor.html>`_
      -- Inherits from ['ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ChromatogramExtractor()
        """
        ...
    
    @overload
    def __init__(self, in_0: ChromatogramExtractor ) -> None:
        """
        Cython signature: void ChromatogramExtractor(ChromatogramExtractor &)
        """
        ...
    
    def extractChromatograms(self, input: MSExperiment , output: MSExperiment , transition_exp: TargetedExperiment , extract_window: float , ppm: bool , trafo: TransformationDescription , rt_extraction_window: float , filter: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void extractChromatograms(MSExperiment & input, MSExperiment & output, TargetedExperiment & transition_exp, double extract_window, bool ppm, TransformationDescription trafo, double rt_extraction_window, String filter)
        Extract chromatograms at the m/z and RT defined by the ExtractionCoordinates
        """
        ...
    
    def setLogType(self, in_0: int ) -> None:
        """
        Cython signature: void setLogType(LogType)
        Sets the progress log that should be used. The default type is NONE!
        """
        ...
    
    def getLogType(self) -> int:
        """
        Cython signature: LogType getLogType()
        Returns the type of progress log being used
        """
        ...
    
    def startProgress(self, begin: int , end: int , label: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void startProgress(ptrdiff_t begin, ptrdiff_t end, String label)
        """
        ...
    
    def setProgress(self, value: int ) -> None:
        """
        Cython signature: void setProgress(ptrdiff_t value)
        Sets the current progress
        """
        ...
    
    def endProgress(self) -> None:
        """
        Cython signature: void endProgress()
        Ends the progress display
        """
        ...
    
    def nextProgress(self) -> None:
        """
        Cython signature: void nextProgress()
        Increment progress by 1 (according to range begin-end)
        """
        ... 


class Compomer:
    """
    Cython implementation of _Compomer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Compomer.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Compomer()
        """
        ...
    
    @overload
    def __init__(self, in_0: Compomer ) -> None:
        """
        Cython signature: void Compomer(Compomer &)
        """
        ...
    
    def add(self, a: Adduct , side: int ) -> None:
        """
        Cython signature: void add(Adduct & a, unsigned int side)
        """
        ...
    
    def isConflicting(self, cmp: Compomer , side_this: int , side_other: int ) -> bool:
        """
        Cython signature: bool isConflicting(Compomer & cmp, unsigned int side_this, unsigned int side_other)
        """
        ...
    
    def setID(self, id: int ) -> None:
        """
        Cython signature: void setID(size_t id)
        Sets an Id which allows unique identification of a compomer
        """
        ...
    
    def getID(self) -> int:
        """
        Cython signature: size_t getID()
        Returns Id which allows unique identification of this compomer
        """
        ...
    
    def getNetCharge(self) -> int:
        """
        Cython signature: int getNetCharge()
        Net charge of compomer (i.e. difference between left and right side of compomer)
        """
        ...
    
    def getMass(self) -> float:
        """
        Cython signature: double getMass()
        Mass of all contained adducts
        """
        ...
    
    def getPositiveCharges(self) -> int:
        """
        Cython signature: int getPositiveCharges()
        Summed positive charges of contained adducts
        """
        ...
    
    def getNegativeCharges(self) -> int:
        """
        Cython signature: int getNegativeCharges()
        Summed negative charges of contained adducts
        """
        ...
    
    def getLogP(self) -> float:
        """
        Cython signature: double getLogP()
        Returns the log probability
        """
        ...
    
    def getRTShift(self) -> float:
        """
        Cython signature: double getRTShift()
        Returns the log probability
        """
        ...
    
    @overload
    def getAdductsAsString(self, ) -> Union[bytes, str, String]:
        """
        Cython signature: String getAdductsAsString()
        Get adducts with their abundance as compact string for both sides
        """
        ...
    
    @overload
    def getAdductsAsString(self, side: int ) -> Union[bytes, str, String]:
        """
        Cython signature: String getAdductsAsString(unsigned int side)
        Get adducts with their abundance as compact string (amounts are absolute unless side=BOTH)
        """
        ...
    
    def isSingleAdduct(self, a: Adduct , side: int ) -> bool:
        """
        Cython signature: bool isSingleAdduct(Adduct & a, unsigned int side)
        Check if Compomer only contains a single adduct on side @p side
        """
        ...
    
    @overload
    def removeAdduct(self, a: Adduct ) -> Compomer:
        """
        Cython signature: Compomer removeAdduct(Adduct & a)
        Remove ALL instances of the given adduct
        """
        ...
    
    @overload
    def removeAdduct(self, a: Adduct , side: int ) -> Compomer:
        """
        Cython signature: Compomer removeAdduct(Adduct & a, unsigned int side)
        """
        ...
    
    def getLabels(self, side: int ) -> List[bytes]:
        """
        Cython signature: StringList getLabels(unsigned int side)
        Returns the adduct labels from parameter(side) given. (LEFT or RIGHT)
        """
        ... 


class ConsensusIDAlgorithmWorst:
    """
    Cython implementation of _ConsensusIDAlgorithmWorst

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ConsensusIDAlgorithmWorst.html>`_
      -- Inherits from ['ConsensusIDAlgorithmIdentity']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void ConsensusIDAlgorithmWorst()
        """
        ...
    
    def apply(self, ids: List[PeptideIdentification] , number_of_runs: int ) -> None:
        """
        Cython signature: void apply(libcpp_vector[PeptideIdentification] & ids, size_t number_of_runs)
        Calculates the consensus ID for a set of peptide identifications of one spectrum or (consensus) feature
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class ConsensusMapNormalizerAlgorithmQuantile:
    """
    Cython implementation of _ConsensusMapNormalizerAlgorithmQuantile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ConsensusMapNormalizerAlgorithmQuantile.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void ConsensusMapNormalizerAlgorithmQuantile()
        """
        ...
    
    def normalizeMaps(self, input_map: ConsensusMap ) -> None:
        """
        Cython signature: void normalizeMaps(ConsensusMap & input_map)
        """
        ...
    
    def resample(self, data_in: List[float] , data_out: List[float] , n_resampling_points: int ) -> None:
        """
        Cython signature: void resample(libcpp_vector[double] & data_in, libcpp_vector[double] & data_out, unsigned int n_resampling_points)
        Resamples data_in and writes the results to data_out
        """
        ...
    
    def extractIntensityVectors(self, map_: ConsensusMap , out_intensities: List[List[float]] ) -> None:
        """
        Cython signature: void extractIntensityVectors(ConsensusMap & map_, libcpp_vector[libcpp_vector[double]] & out_intensities)
        Extracts the intensities of the features of the different maps
        """
        ...
    
    def setNormalizedIntensityValues(self, feature_ints: List[List[float]] , map_: ConsensusMap ) -> None:
        """
        Cython signature: void setNormalizedIntensityValues(libcpp_vector[libcpp_vector[double]] & feature_ints, ConsensusMap & map_)
        Writes the intensity values in feature_ints to the corresponding features in map
        """
        ... 


class ConvexHull2D:
    """
    Cython implementation of _ConvexHull2D

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ConvexHull2D.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ConvexHull2D()
        """
        ...
    
    @overload
    def __init__(self, in_0: ConvexHull2D ) -> None:
        """
        Cython signature: void ConvexHull2D(ConvexHull2D &)
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        Removes all points
        """
        ...
    
    def compress(self) -> int:
        """
        Cython signature: size_t compress()
        Allows to reduce the disk/memory footprint of a hull
        """
        ...
    
    def expandToBoundingBox(self) -> None:
        """
        Cython signature: void expandToBoundingBox()
        Expand a convex hull to its bounding box.
        """
        ...
    
    def addPoint(self, point: Union[Sequence[int], Sequence[float]] ) -> bool:
        """
        Cython signature: bool addPoint(DPosition2 point)
        Adds a point to the hull if it is not already contained. Returns if the point was added. This will trigger recomputation of the outer hull points (thus points set with setHullPoints() will be lost)
        """
        ...
    
    def addPoints(self, points: '_np.ndarray[Any, _np.dtype[_np.float32]]' ) -> None:
        """
        Cython signature: void addPoints(libcpp_vector[DPosition2] points)
        Adds points to the hull if it is not already contained. This will trigger recomputation of the outer hull points (thus points set with setHullPoints() will be lost)
        """
        ...
    
    def encloses(self, in_0: Union[Sequence[int], Sequence[float]] ) -> bool:
        """
        Cython signature: bool encloses(DPosition2)
        Returns if the `point` lies in the feature hull
        """
        ...
    
    def getHullPoints(self) -> '_np.ndarray[Any, _np.dtype[_np.float32]]':
        """
        Cython signature: libcpp_vector[DPosition2] getHullPoints()
        Accessor for the outer points
        """
        ...
    
    def setHullPoints(self, in_0: '_np.ndarray[Any, _np.dtype[_np.float32]]' ) -> None:
        """
        Cython signature: void setHullPoints(libcpp_vector[DPosition2])
        Accessor for the outer(!) points (no checking is performed if this is actually a convex hull)
        """
        ...
    
    def getBoundingBox(self) -> DBoundingBox2:
        """
        Cython signature: DBoundingBox2 getBoundingBox()
        Returns the bounding box of the feature hull points
        """
        ...
    
    def __richcmp__(self, other: ConvexHull2D, op: int) -> Any:
        ... 


class CsiAdapterHit:
    """
    Cython implementation of _CsiAdapterHit

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::CsiFingerIdMzTabWriter_1_1CsiAdapterHit.html>`_
    """
    
    inchikey2D: Union[bytes, str, String]
    
    inchi: Union[bytes, str, String]
    
    rank: int
    
    formula_rank: int
    
    adduct: Union[bytes, str, String]
    
    molecular_formula: Union[bytes, str, String]
    
    score: float
    
    name: Union[bytes, str, String]
    
    smiles: Union[bytes, str, String]
    
    xlogp: Union[bytes, str, String]
    
    dbflags: Union[bytes, str, String]
    
    pubchemids: List[bytes]
    
    links: List[bytes]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CsiAdapterHit()
        """
        ...
    
    @overload
    def __init__(self, in_0: CsiAdapterHit ) -> None:
        """
        Cython signature: void CsiAdapterHit(CsiAdapterHit &)
        """
        ... 


class DTAFile:
    """
    Cython implementation of _DTAFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DTAFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void DTAFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: DTAFile ) -> None:
        """
        Cython signature: void DTAFile(DTAFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , spectrum: MSSpectrum ) -> None:
        """
        Cython signature: void load(String filename, MSSpectrum & spectrum)
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , spectrum: MSSpectrum ) -> None:
        """
        Cython signature: void store(String filename, MSSpectrum & spectrum)
        """
        ... 


class DataValue:
    """
    Cython implementation of _DataValue

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DataValue.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void DataValue()
        """
        ...
    
    @overload
    def __init__(self, in_0: DataValue ) -> None:
        """
        Cython signature: void DataValue(DataValue &)
        """
        ...
    
    @overload
    def __init__(self, in_0: bytes ) -> None:
        """
        Cython signature: void DataValue(char *)
        """
        ...
    
    @overload
    def __init__(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void DataValue(const String &)
        """
        ...
    
    @overload
    def __init__(self, in_0: int ) -> None:
        """
        Cython signature: void DataValue(int)
        """
        ...
    
    @overload
    def __init__(self, in_0: float ) -> None:
        """
        Cython signature: void DataValue(double)
        """
        ...
    
    @overload
    def __init__(self, in_0: List[bytes] ) -> None:
        """
        Cython signature: void DataValue(StringList)
        """
        ...
    
    @overload
    def __init__(self, in_0: List[int] ) -> None:
        """
        Cython signature: void DataValue(IntList)
        """
        ...
    
    @overload
    def __init__(self, in_0: List[float] ) -> None:
        """
        Cython signature: void DataValue(DoubleList)
        """
        ...
    
    @overload
    def __init__(self, in_0: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void DataValue(ParamValue)
        """
        ...
    
    def toStringList(self) -> List[bytes]:
        """
        Cython signature: StringList toStringList()
        """
        ...
    
    def toDoubleList(self) -> List[float]:
        """
        Cython signature: libcpp_vector[double] toDoubleList()
        """
        ...
    
    def toIntList(self) -> List[int]:
        """
        Cython signature: libcpp_vector[int] toIntList()
        """
        ...
    
    def toString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        """
        ...
    
    def toBool(self) -> bool:
        """
        Cython signature: bool toBool()
        """
        ...
    
    def valueType(self) -> int:
        """
        Cython signature: DataType valueType()
        """
        ...
    
    def isEmpty(self) -> int:
        """
        Cython signature: int isEmpty()
        """
        ...
    
    def getUnitType(self) -> int:
        """
        Cython signature: UnitType getUnitType()
        """
        ...
    
    def setUnitType(self, u: int ) -> None:
        """
        Cython signature: void setUnitType(UnitType u)
        """
        ...
    
    def hasUnit(self) -> bool:
        """
        Cython signature: bool hasUnit()
        """
        ...
    
    def getUnit(self) -> int:
        """
        Cython signature: int getUnit()
        """
        ...
    
    def setUnit(self, unit_id: int ) -> None:
        """
        Cython signature: void setUnit(int unit_id)
        """
        ...
    
    def __str__(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        """
        ... 


class Element:
    """
    Cython implementation of _Element

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Element.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Element()
        """
        ...
    
    @overload
    def __init__(self, in_0: Element ) -> None:
        """
        Cython signature: void Element(Element &)
        """
        ...
    
    @overload
    def __init__(self, name: Union[bytes, str, String] , symbol: Union[bytes, str, String] , atomic_number: int , average_weight: float , mono_weight: float , isotopes: IsotopeDistribution ) -> None:
        """
        Cython signature: void Element(String name, String symbol, unsigned int atomic_number, double average_weight, double mono_weight, IsotopeDistribution isotopes)
        """
        ...
    
    def setAtomicNumber(self, atomic_number: int ) -> None:
        """
        Cython signature: void setAtomicNumber(unsigned int atomic_number)
        Sets unique atomic number
        """
        ...
    
    def getAtomicNumber(self) -> int:
        """
        Cython signature: unsigned int getAtomicNumber()
        Returns the unique atomic number
        """
        ...
    
    def setAverageWeight(self, weight: float ) -> None:
        """
        Cython signature: void setAverageWeight(double weight)
        Sets the average weight of the element
        """
        ...
    
    def getAverageWeight(self) -> float:
        """
        Cython signature: double getAverageWeight()
        Returns the average weight of the element
        """
        ...
    
    def setMonoWeight(self, weight: float ) -> None:
        """
        Cython signature: void setMonoWeight(double weight)
        Sets the mono isotopic weight of the element
        """
        ...
    
    def getMonoWeight(self) -> float:
        """
        Cython signature: double getMonoWeight()
        Returns the mono isotopic weight of the element
        """
        ...
    
    def setIsotopeDistribution(self, isotopes: IsotopeDistribution ) -> None:
        """
        Cython signature: void setIsotopeDistribution(IsotopeDistribution isotopes)
        Sets the isotope distribution of the element
        """
        ...
    
    def getIsotopeDistribution(self) -> IsotopeDistribution:
        """
        Cython signature: IsotopeDistribution getIsotopeDistribution()
        Returns the isotope distribution of the element
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(String name)
        Sets the name of the element
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name of the element
        """
        ...
    
    def setSymbol(self, symbol: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setSymbol(String symbol)
        Sets symbol of the element
        """
        ...
    
    def getSymbol(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getSymbol()
        Returns symbol of the element
        """
        ... 


class EmpiricalFormula:
    """
    Cython implementation of _EmpiricalFormula

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1EmpiricalFormula.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void EmpiricalFormula()
        Representation of an empirical formula
        """
        ...
    
    @overload
    def __init__(self, in_0: EmpiricalFormula ) -> None:
        """
        Cython signature: void EmpiricalFormula(EmpiricalFormula &)
        """
        ...
    
    @overload
    def __init__(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void EmpiricalFormula(String)
        EmpiricalFormula Constructor from string
        """
        ...
    
    @overload
    def __init__(self, number: int , element: Element , charge: int ) -> None:
        """
        Cython signature: void EmpiricalFormula(ptrdiff_t number, Element * element, ptrdiff_t charge)
        EmpiricalFormula Constructor with element pointer and number
        """
        ...
    
    def getMonoWeight(self) -> float:
        """
        Cython signature: double getMonoWeight()
        Returns the mono isotopic weight of the formula (includes proton charges)
        """
        ...
    
    def getAverageWeight(self) -> float:
        """
        Cython signature: double getAverageWeight()
        Returns the average weight of the formula (includes proton charges)
        """
        ...
    
    def estimateFromWeightAndComp(self, average_weight: float , C: float , H: float , N: float , O: float , S: float , P: float ) -> bool:
        """
        Cython signature: bool estimateFromWeightAndComp(double average_weight, double C, double H, double N, double O, double S, double P)
        Fills this EmpiricalFormula with an approximate elemental composition for a given average weight and approximate elemental stoichiometry
        """
        ...
    
    def estimateFromWeightAndCompAndS(self, average_weight: float , S: int , C: float , H: float , N: float , O: float , P: float ) -> bool:
        """
        Cython signature: bool estimateFromWeightAndCompAndS(double average_weight, unsigned int S, double C, double H, double N, double O, double P)
        Fills this EmpiricalFormula with an approximate elemental composition for a given average weight, exact number of sulfurs, and approximate elemental stoichiometry
        """
        ...
    
    @overload
    def getIsotopeDistribution(self, in_0: CoarseIsotopePatternGenerator ) -> IsotopeDistribution:
        """
        Cython signature: IsotopeDistribution getIsotopeDistribution(CoarseIsotopePatternGenerator)
        Computes the isotope distribution of an empirical formula using the CoarseIsotopePatternGenerator or the FineIsotopePatternGenerator method
        """
        ...
    
    @overload
    def getIsotopeDistribution(self, in_0: FineIsotopePatternGenerator ) -> IsotopeDistribution:
        """
        Cython signature: IsotopeDistribution getIsotopeDistribution(FineIsotopePatternGenerator)
        """
        ...
    
    def getConditionalFragmentIsotopeDist(self, precursor: EmpiricalFormula , precursor_isotopes: Set[int] , method: CoarseIsotopePatternGenerator ) -> IsotopeDistribution:
        """
        Cython signature: IsotopeDistribution getConditionalFragmentIsotopeDist(EmpiricalFormula & precursor, libcpp_set[unsigned int] & precursor_isotopes, CoarseIsotopePatternGenerator method)
        """
        ...
    
    def getNumberOfAtoms(self) -> int:
        """
        Cython signature: size_t getNumberOfAtoms()
        Returns the total number of atoms
        """
        ...
    
    def getCharge(self) -> int:
        """
        Cython signature: ptrdiff_t getCharge()
        Returns the total charge
        """
        ...
    
    def setCharge(self, charge: int ) -> None:
        """
        Cython signature: void setCharge(ptrdiff_t charge)
        Sets the charge
        """
        ...
    
    def toString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        Returns the formula as a string (charges are not included)
        """
        ...
    
    def getElementalComposition(self) -> Dict[bytes, int]:
        """
        Cython signature: libcpp_map[libcpp_string,int] getElementalComposition()
        Get elemental composition as a hash {'Symbol' -> NrAtoms}
        """
        ...
    
    def isEmpty(self) -> bool:
        """
        Cython signature: bool isEmpty()
        Returns true if the formula does not contain a element
        """
        ...
    
    def isCharged(self) -> bool:
        """
        Cython signature: bool isCharged()
        Returns true if charge is not equal to zero
        """
        ...
    
    def hasElement(self, element: Element ) -> bool:
        """
        Cython signature: bool hasElement(Element * element)
        Returns true if the formula contains the element
        """
        ...
    
    def contains(self, ef: EmpiricalFormula ) -> bool:
        """
        Cython signature: bool contains(EmpiricalFormula ef)
        Returns true if all elements from `ef` ( empirical formula ) are LESS abundant (negative allowed) than the corresponding elements of this EmpiricalFormula
        """
        ...
    
    def __add__(self: EmpiricalFormula, other: EmpiricalFormula) -> EmpiricalFormula:
        ...
    
    def __sub__(self: EmpiricalFormula, other: EmpiricalFormula) -> EmpiricalFormula:
        ...
    
    def __iadd__(self: EmpiricalFormula, other: EmpiricalFormula) -> EmpiricalFormula:
        ...
    
    def __isub__(self: EmpiricalFormula, other: EmpiricalFormula) -> EmpiricalFormula:
        ...
    
    def calculateTheoreticalIsotopesNumber(self) -> float:
        """
        Cython signature: double calculateTheoreticalIsotopesNumber()
        """
        ...
    
    def __str__(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        Returns the formula as a string (charges are not included)
        """
        ...
    
    def __richcmp__(self, other: EmpiricalFormula, op: int) -> Any:
        ... 


class EnzymaticDigestion:
    """
    Cython implementation of _EnzymaticDigestion

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1EnzymaticDigestion.html>`_

      Class for the enzymatic digestion of proteins
    
      Digestion can be performed using simple regular expressions, e.g. [KR] | [^P] for trypsin.
      Also missed cleavages can be modeled, i.e. adjacent peptides are not cleaved
      due to enzyme malfunction/access restrictions. If n missed cleavages are allowed, all possible resulting
      peptides (cleaved and uncleaved) with up to n missed cleavages are returned.
      Thus no random selection of just n specific missed cleavage sites is performed.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void EnzymaticDigestion()
        """
        ...
    
    @overload
    def __init__(self, in_0: EnzymaticDigestion ) -> None:
        """
        Cython signature: void EnzymaticDigestion(EnzymaticDigestion &)
        """
        ...
    
    def getMissedCleavages(self) -> int:
        """
        Cython signature: size_t getMissedCleavages()
        Returns the max. number of allowed missed cleavages for the digestion
        """
        ...
    
    def setMissedCleavages(self, missed_cleavages: int ) -> None:
        """
        Cython signature: void setMissedCleavages(size_t missed_cleavages)
        Sets the max. number of allowed missed cleavages for the digestion (default is 0). This setting is ignored when log model is used
        """
        ...
    
    def countInternalCleavageSites(self, sequence: Union[bytes, str, String] ) -> int:
        """
        Cython signature: size_t countInternalCleavageSites(String sequence)
        Returns the number of internal cleavage sites for this sequence.
        """
        ...
    
    def getEnzymeName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getEnzymeName()
        Returns the enzyme for the digestion
        """
        ...
    
    def setEnzyme(self, enzyme: DigestionEnzyme ) -> None:
        """
        Cython signature: void setEnzyme(DigestionEnzyme * enzyme)
        Sets the enzyme for the digestion
        """
        ...
    
    def getSpecificity(self) -> int:
        """
        Cython signature: Specificity getSpecificity()
        Returns the specificity for the digestion
        """
        ...
    
    def setSpecificity(self, spec: int ) -> None:
        """
        Cython signature: void setSpecificity(Specificity spec)
        Sets the specificity for the digestion (default is SPEC_FULL)
        """
        ...
    
    def getSpecificityByName(self, name: Union[bytes, str, String] ) -> int:
        """
        Cython signature: Specificity getSpecificityByName(String name)
        Returns the specificity by name. Returns SPEC_UNKNOWN if name is not valid
        """
        ...
    
    def digestUnmodified(self, sequence: StringView , output: List[StringView] , min_length: int , max_length: int ) -> int:
        """
        Cython signature: size_t digestUnmodified(StringView sequence, libcpp_vector[StringView] & output, size_t min_length, size_t max_length)
        Performs the enzymatic digestion of an unmodified sequence\n
        By returning only references into the original string this is very fast
        
        
        :param sequence: Sequence to digest
        :param output: Digestion products
        :param min_length: Minimal length of reported products
        :param max_length: Maximal length of reported products (0 = no restriction)
        :return: Number of discarded digestion products (which are not matching length restrictions)
        """
        ...
    
    def isValidProduct(self, sequence: Union[bytes, str, String] , pos: int , length: int , ignore_missed_cleavages: bool ) -> bool:
        """
        Cython signature: bool isValidProduct(String sequence, int pos, int length, bool ignore_missed_cleavages)
        Boolean operator returns true if the peptide fragment starting at position `pos` with length `length` within the sequence `sequence` generated by the current enzyme\n
        Checks if peptide is a valid digestion product of the enzyme, taking into account specificity and the MC flag provided here
        
        
        :param protein: Protein sequence
        :param pep_pos: Starting index of potential peptide
        :param pep_length: Length of potential peptide
        :param ignore_missed_cleavages: Do not compare MC's of potential peptide to the maximum allowed MC's
        :return: True if peptide has correct n/c terminals (according to enzyme, specificity and missed cleavages)
        """
        ...
    Specificity : __Specificity 


class FalseDiscoveryRate:
    """
    Cython implementation of _FalseDiscoveryRate

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FalseDiscoveryRate.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void FalseDiscoveryRate()
        """
        ...
    
    @overload
    def apply(self, forward_ids: List[PeptideIdentification] , reverse_ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void apply(libcpp_vector[PeptideIdentification] & forward_ids, libcpp_vector[PeptideIdentification] & reverse_ids)
        """
        ...
    
    @overload
    def apply(self, id: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void apply(libcpp_vector[PeptideIdentification] & id)
        """
        ...
    
    @overload
    def apply(self, forward_ids: List[ProteinIdentification] , reverse_ids: List[ProteinIdentification] ) -> None:
        """
        Cython signature: void apply(libcpp_vector[ProteinIdentification] & forward_ids, libcpp_vector[ProteinIdentification] & reverse_ids)
        """
        ...
    
    @overload
    def apply(self, id: List[ProteinIdentification] ) -> None:
        """
        Cython signature: void apply(libcpp_vector[ProteinIdentification] & id)
        """
        ...
    
    def applyEstimated(self, ids: List[ProteinIdentification] ) -> None:
        """
        Cython signature: void applyEstimated(libcpp_vector[ProteinIdentification] & ids)
        """
        ...
    
    @overload
    def applyEvaluateProteinIDs(self, ids: List[ProteinIdentification] , pepCutoff: float , fpCutoff: int , diffWeight: float ) -> float:
        """
        Cython signature: double applyEvaluateProteinIDs(libcpp_vector[ProteinIdentification] & ids, double pepCutoff, unsigned int fpCutoff, double diffWeight)
        """
        ...
    
    @overload
    def applyEvaluateProteinIDs(self, ids: ProteinIdentification , pepCutoff: float , fpCutoff: int , diffWeight: float ) -> float:
        """
        Cython signature: double applyEvaluateProteinIDs(ProteinIdentification & ids, double pepCutoff, unsigned int fpCutoff, double diffWeight)
        """
        ...
    
    @overload
    def applyBasic(self, run_info: List[ProteinIdentification] , ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void applyBasic(libcpp_vector[ProteinIdentification] & run_info, libcpp_vector[PeptideIdentification] & ids)
        """
        ...
    
    @overload
    def applyBasic(self, ids: List[PeptideIdentification] , higher_score_better: bool , charge: int , identifier: Union[bytes, str, String] , only_best_per_pep: bool ) -> None:
        """
        Cython signature: void applyBasic(libcpp_vector[PeptideIdentification] & ids, bool higher_score_better, int charge, String identifier, bool only_best_per_pep)
        """
        ...
    
    @overload
    def applyBasic(self, cmap: ConsensusMap , use_unassigned_peptides: bool ) -> None:
        """
        Cython signature: void applyBasic(ConsensusMap & cmap, bool use_unassigned_peptides)
        """
        ...
    
    @overload
    def applyBasic(self, id: ProteinIdentification , groups_too: bool ) -> None:
        """
        Cython signature: void applyBasic(ProteinIdentification & id, bool groups_too)
        """
        ...
    
    def applyPickedProteinFDR(self, id: ProteinIdentification , decoy_string: String , decoy_prefix: bool , groups_too: bool ) -> None:
        """
        Cython signature: void applyPickedProteinFDR(ProteinIdentification & id, String & decoy_string, bool decoy_prefix, bool groups_too)
        """
        ...
    
    @overload
    def rocN(self, ids: List[PeptideIdentification] , fp_cutoff: int ) -> float:
        """
        Cython signature: double rocN(libcpp_vector[PeptideIdentification] & ids, size_t fp_cutoff)
        """
        ...
    
    @overload
    def rocN(self, ids: ConsensusMap , fp_cutoff: int , include_unassigned_peptides: bool ) -> float:
        """
        Cython signature: double rocN(ConsensusMap & ids, size_t fp_cutoff, bool include_unassigned_peptides)
        """
        ...
    
    @overload
    def rocN(self, ids: ConsensusMap , fp_cutoff: int , identifier: Union[bytes, str, String] , include_unassigned_peptides: bool ) -> float:
        """
        Cython signature: double rocN(ConsensusMap & ids, size_t fp_cutoff, const String & identifier, bool include_unassigned_peptides)
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class FeatureFinderAlgorithmIsotopeWavelet:
    """
    Cython implementation of _FeatureFinderAlgorithmIsotopeWavelet

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureFinderAlgorithmIsotopeWavelet.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void FeatureFinderAlgorithmIsotopeWavelet()
        """
        ...
    
    def setData(self, input: MSExperiment , output: FeatureMap , ff: FeatureFinder ) -> None:
        """
        Cython signature: void setData(MSExperiment & input, FeatureMap & output, FeatureFinder & ff)
        """
        ...
    
    def run(self) -> None:
        """
        Cython signature: void run()
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ...
    
    getProductName: __static_FeatureFinderAlgorithmIsotopeWavelet_getProductName 


class FeatureFinderMultiplexAlgorithm:
    """
    Cython implementation of _FeatureFinderMultiplexAlgorithm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureFinderMultiplexAlgorithm.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FeatureFinderMultiplexAlgorithm()
        """
        ...
    
    @overload
    def __init__(self, in_0: FeatureFinderMultiplexAlgorithm ) -> None:
        """
        Cython signature: void FeatureFinderMultiplexAlgorithm(FeatureFinderMultiplexAlgorithm &)
        """
        ...
    
    def run(self, exp: MSExperiment , progress: bool ) -> None:
        """
        Cython signature: void run(MSExperiment & exp, bool progress)
        Main method for feature detection
        """
        ...
    
    def getFeatureMap(self) -> FeatureMap:
        """
        Cython signature: FeatureMap getFeatureMap()
        """
        ...
    
    def getConsensusMap(self) -> ConsensusMap:
        """
        Cython signature: ConsensusMap getConsensusMap()
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class FeatureGroupingAlgorithmLabeled:
    """
    Cython implementation of _FeatureGroupingAlgorithmLabeled

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureGroupingAlgorithmLabeled.html>`_
      -- Inherits from ['FeatureGroupingAlgorithm']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void FeatureGroupingAlgorithmLabeled()
        """
        ...
    
    def group(self, maps: List[FeatureMap] , out: ConsensusMap ) -> None:
        """
        Cython signature: void group(libcpp_vector[FeatureMap] & maps, ConsensusMap & out)
        """
        ...
    
    def getProductName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getProductName()
        """
        ...
    
    def transferSubelements(self, maps: List[ConsensusMap] , out: ConsensusMap ) -> None:
        """
        Cython signature: void transferSubelements(libcpp_vector[ConsensusMap] maps, ConsensusMap & out)
        Transfers subelements (grouped features) from input consensus maps to the result consensus map
        """
        ...
    
    def registerChildren(self) -> None:
        """
        Cython signature: void registerChildren()
        Register all derived classes in this method
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class FileTypes:
    """
    Cython implementation of _FileTypes

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FileTypes.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FileTypes()
        Centralizes the file types recognized by FileHandler
        """
        ...
    
    @overload
    def __init__(self, in_0: FileTypes ) -> None:
        """
        Cython signature: void FileTypes(FileTypes &)
        """
        ...
    
    def typeToName(self, t: int ) -> Union[bytes, str, String]:
        """
        Cython signature: String typeToName(FileType t)
        Returns the name/extension of the type
        """
        ...
    
    def typeToMZML(self, t: int ) -> Union[bytes, str, String]:
        """
        Cython signature: String typeToMZML(FileType t)
        Returns the mzML name
        """
        ...
    
    def nameToType(self, name: Union[bytes, str, String] ) -> int:
        """
        Cython signature: FileType nameToType(String name)
        Converts a file type name into a Type
        
        
        :param name: A case-insensitive name (e.g. FASTA or Fasta, etc.)
        """
        ... 


class HyperScore:
    """
    Cython implementation of _HyperScore

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1HyperScore.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void HyperScore()
        An implementation of the X!Tandem HyperScore PSM scoring function
        """
        ...
    
    @overload
    def __init__(self, in_0: HyperScore ) -> None:
        """
        Cython signature: void HyperScore(HyperScore &)
        """
        ...
    
    def compute(self, fragment_mass_tolerance: float , fragment_mass_tolerance_unit_ppm: bool , exp_spectrum: MSSpectrum , theo_spectrum: MSSpectrum ) -> float:
        """
        Cython signature: double compute(double fragment_mass_tolerance, bool fragment_mass_tolerance_unit_ppm, MSSpectrum & exp_spectrum, MSSpectrum & theo_spectrum)
        Compute the (ln transformed) X!Tandem HyperScore\n
        
        1. the dot product of peak intensities between matching peaks in experimental and theoretical spectrum is calculated
        2. the HyperScore is calculated from the dot product by multiplying by factorials of matching b- and y-ions
        
        
        :note: Peak intensities of the theoretical spectrum are typically 1 or TIC normalized, but can also be e.g. ion probabilities
        :param fragment_mass_tolerance: Mass tolerance applied left and right of the theoretical spectrum peak position
        :param fragment_mass_tolerance_unit_ppm: Unit of the mass tolerance is: Thomson if false, ppm if true
        :param exp_spectrum: Measured spectrum
        :param theo_spectrum: Theoretical spectrum Peaks need to contain an ion annotation as provided by TheoreticalSpectrumGenerator
        """
        ... 


class IDRipper:
    """
    Cython implementation of _IDRipper

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::IDRipper_1_1IDRipper.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void IDRipper()
        Ripping protein/peptide identification according their file origin
        """
        ...
    
    def rip(self, rfis: List[RipFileIdentifier] , rfcs: List[RipFileContent] , proteins: List[ProteinIdentification] , peptides: List[PeptideIdentification] , full_split: bool , split_ident_runs: bool ) -> None:
        """
        Cython signature: void rip(libcpp_vector[RipFileIdentifier] & rfis, libcpp_vector[RipFileContent] & rfcs, libcpp_vector[ProteinIdentification] & proteins, libcpp_vector[PeptideIdentification] & peptides, bool full_split, bool split_ident_runs)
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class IdentificationRuns:
    """
    Cython implementation of _IdentificationRuns

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::IDRipper_1_1IdentificationRuns.html>`_
    """
    
    def __init__(self, prot_ids: List[ProteinIdentification] ) -> None:
        """
        Cython signature: void IdentificationRuns(libcpp_vector[ProteinIdentification] & prot_ids)
        """
        ... 


class InclusionExclusionList:
    """
    Cython implementation of _InclusionExclusionList

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1InclusionExclusionList.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void InclusionExclusionList()
        Provides functionality for writing inclusion or exclusion lists
        """
        ...
    
    @overload
    def __init__(self, in_0: InclusionExclusionList ) -> None:
        """
        Cython signature: void InclusionExclusionList(InclusionExclusionList &)
        """
        ...
    
    @overload
    def writeTargets(self, fasta_entries: List[FASTAEntry] , out_path: Union[bytes, str, String] , charges: List[int] , rt_model_path: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void writeTargets(libcpp_vector[FASTAEntry] & fasta_entries, const String & out_path, IntList & charges, const String rt_model_path)
        Writes inclusion or exclusion list of tryptic peptides of the given proteins (tab-delimited)
        """
        ...
    
    @overload
    def writeTargets(self, map_: FeatureMap , out_path: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void writeTargets(FeatureMap & map_, const String & out_path)
        Writes inclusion or exclusion list of given feature map
        """
        ...
    
    @overload
    def writeTargets(self, pep_ids: List[PeptideIdentification] , out_path: Union[bytes, str, String] , charges: List[int] ) -> None:
        """
        Cython signature: void writeTargets(libcpp_vector[PeptideIdentification] & pep_ids, const String & out_path, IntList & charges)
        Writes inclusion or exclusion list of given peptide ids (tab-delimited)
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class IndexedMzMLFileLoader:
    """
    Cython implementation of _IndexedMzMLFileLoader

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IndexedMzMLFileLoader.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void IndexedMzMLFileLoader()
        A class to load an indexedmzML file
        """
        ...
    
    def load(self, in_0: Union[bytes, str, String] , in_1: OnDiscMSExperiment ) -> bool:
        """
        Cython signature: bool load(String, OnDiscMSExperiment &)
        Load a file\n
        
        Tries to parse the file, success needs to be checked with the return value
        """
        ...
    
    @overload
    def store(self, in_0: Union[bytes, str, String] , in_1: OnDiscMSExperiment ) -> None:
        """
        Cython signature: void store(String, OnDiscMSExperiment &)
        Store a file from an on-disc data-structure
        
        
        :param filename: Filename determines where the file will be stored
        :param exp: MS data to be stored
        """
        ...
    
    @overload
    def store(self, in_0: Union[bytes, str, String] , in_1: MSExperiment ) -> None:
        """
        Cython signature: void store(String, MSExperiment &)
        Store a file from an in-memory data-structure
        
        
        :param filename: Filename determines where the file will be stored
        :param exp: MS data to be stored
        """
        ...
    
    def getOptions(self) -> PeakFileOptions:
        """
        Cython signature: PeakFileOptions getOptions()
        Returns the options for loading/storing
        """
        ...
    
    def setOptions(self, in_0: PeakFileOptions ) -> None:
        """
        Cython signature: void setOptions(PeakFileOptions)
        Returns the options for loading/storing
        """
        ... 


class InspectInfile:
    """
    Cython implementation of _InspectInfile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1InspectInfile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void InspectInfile()
        Inspect input file adapter
        """
        ...
    
    @overload
    def __init__(self, in_0: InspectInfile ) -> None:
        """
        Cython signature: void InspectInfile(InspectInfile &)
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void store(const String & filename)
        Stores the experiment data in an Inspect input file that can be used as input for Inspect shell execution
        """
        ...
    
    def handlePTMs(self, modification_line: Union[bytes, str, String] , modifications_filename: Union[bytes, str, String] , monoisotopic: bool ) -> None:
        """
        Cython signature: void handlePTMs(const String & modification_line, const String & modifications_filename, bool monoisotopic)
        Retrieves the name, mass change, affected residues, type and position for all modifications from a string
        
        
        :param modification_line:
        :param modifications_filename:
        :param monoisotopic: if true, masses are considered to be monoisotopic
        :raises:
          Exception: FileNotReadable if the modifications_filename could not be read
        :raises:
          Exception: FileNotFound if modifications_filename could not be found
        :raises:
          Exception: ParseError if modifications_filename could not be parsed
        """
        ...
    
    def getSpectra(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getSpectra()
        Specifies a spectrum file to search
        """
        ...
    
    def setSpectra(self, spectra: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setSpectra(const String & spectra)
        Specifies a spectrum file to search
        """
        ...
    
    def getDb(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getDb()
        Specifies the name of a database (.trie file) to search
        """
        ...
    
    def setDb(self, db: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setDb(const String & db)
        Specifies the name of a database (.trie file) to search
        """
        ...
    
    def getEnzyme(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getEnzyme()
        Specifies the name of a enzyme. "Trypsin", "None", and "Chymotrypsin" are the available values
        """
        ...
    
    def setEnzyme(self, enzyme: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setEnzyme(const String & enzyme)
        Specifies the name of a enzyme. "Trypsin", "None", and "Chymotrypsin" are the available values
        """
        ...
    
    def getModificationsPerPeptide(self) -> int:
        """
        Cython signature: int getModificationsPerPeptide()
        Number of PTMs permitted in a single peptide
        """
        ...
    
    def setModificationsPerPeptide(self, modifications_per_peptide: int ) -> None:
        """
        Cython signature: void setModificationsPerPeptide(int modifications_per_peptide)
        Number of PTMs permitted in a single peptide
        """
        ...
    
    def getBlind(self) -> int:
        """
        Cython signature: unsigned int getBlind()
        Run inspect in a blind mode
        """
        ...
    
    def setBlind(self, blind: int ) -> None:
        """
        Cython signature: void setBlind(unsigned int blind)
        Run inspect in a blind mode
        """
        ...
    
    def getMaxPTMsize(self) -> float:
        """
        Cython signature: float getMaxPTMsize()
        The maximum modification size (in Da) to consider in a blind search
        """
        ...
    
    def setMaxPTMsize(self, maxptmsize: float ) -> None:
        """
        Cython signature: void setMaxPTMsize(float maxptmsize)
        The maximum modification size (in Da) to consider in a blind search
        """
        ...
    
    def getPrecursorMassTolerance(self) -> float:
        """
        Cython signature: float getPrecursorMassTolerance()
        Specifies the parent mass tolerance, in Daltons
        """
        ...
    
    def setPrecursorMassTolerance(self, precursor_mass_tolerance: float ) -> None:
        """
        Cython signature: void setPrecursorMassTolerance(float precursor_mass_tolerance)
        Specifies the parent mass tolerance, in Daltons
        """
        ...
    
    def getPeakMassTolerance(self) -> float:
        """
        Cython signature: float getPeakMassTolerance()
        How far b and y peaks can be shifted from their expected masses.
        """
        ...
    
    def setPeakMassTolerance(self, peak_mass_tolerance: float ) -> None:
        """
        Cython signature: void setPeakMassTolerance(float peak_mass_tolerance)
        How far b and y peaks can be shifted from their expected masses
        """
        ...
    
    def getMulticharge(self) -> int:
        """
        Cython signature: unsigned int getMulticharge()
        If set to true, attempt to guess the precursor charge and mass, and consider multiple charge states if feasible
        """
        ...
    
    def setMulticharge(self, multicharge: int ) -> None:
        """
        Cython signature: void setMulticharge(unsigned int multicharge)
        If set to true, attempt to guess the precursor charge and mass, and consider multiple charge states if feasible
        """
        ...
    
    def getInstrument(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getInstrument()
        If set to QTOF, uses a QTOF-derived fragmentation model, and does not attempt to correct the parent mass
        """
        ...
    
    def setInstrument(self, instrument: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setInstrument(const String & instrument)
        If set to QTOF, uses a QTOF-derived fragmentation model, and does not attempt to correct the parent mass
        """
        ...
    
    def getTagCount(self) -> int:
        """
        Cython signature: int getTagCount()
        Number of tags to generate
        """
        ...
    
    def setTagCount(self, TagCount: int ) -> None:
        """
        Cython signature: void setTagCount(int TagCount)
        Number of tags to generate
        """
        ...
    
    def __richcmp__(self, other: InspectInfile, op: int) -> Any:
        ... 


class InstrumentSettings:
    """
    Cython implementation of _InstrumentSettings

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1InstrumentSettings.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void InstrumentSettings()
        Description of the settings a MS Instrument was run with
        """
        ...
    
    @overload
    def __init__(self, in_0: InstrumentSettings ) -> None:
        """
        Cython signature: void InstrumentSettings(InstrumentSettings &)
        """
        ...
    
    def getPolarity(self) -> int:
        """
        Cython signature: Polarity getPolarity()
        Returns the polarity
        """
        ...
    
    def setPolarity(self, in_0: int ) -> None:
        """
        Cython signature: void setPolarity(Polarity)
        Sets the polarity
        """
        ...
    
    def getScanMode(self) -> int:
        """
        Cython signature: ScanMode getScanMode()
        Returns the scan mode
        """
        ...
    
    def setScanMode(self, scan_mode: int ) -> None:
        """
        Cython signature: void setScanMode(ScanMode scan_mode)
        Sets the scan mode
        """
        ...
    
    def getZoomScan(self) -> bool:
        """
        Cython signature: bool getZoomScan()
        Returns if this scan is a zoom (enhanced resolution) scan
        """
        ...
    
    def setZoomScan(self, zoom_scan: bool ) -> None:
        """
        Cython signature: void setZoomScan(bool zoom_scan)
        Sets if this scan is a zoom (enhanced resolution) scan
        """
        ...
    
    def getScanWindows(self) -> List[ScanWindow]:
        """
        Cython signature: libcpp_vector[ScanWindow] getScanWindows()
        Returns the m/z scan windows
        """
        ...
    
    def setScanWindows(self, scan_windows: List[ScanWindow] ) -> None:
        """
        Cython signature: void setScanWindows(libcpp_vector[ScanWindow] scan_windows)
        Sets the m/z scan windows
        """
        ...
    
    def isMetaEmpty(self) -> bool:
        """
        Cython signature: bool isMetaEmpty()
        Returns if the MetaInfo is empty
        """
        ...
    
    def clearMetaInfo(self) -> None:
        """
        Cython signature: void clearMetaInfo()
        Removes all meta values
        """
        ...
    
    def metaRegistry(self) -> MetaInfoRegistry:
        """
        Cython signature: MetaInfoRegistry metaRegistry()
        Returns a reference to the MetaInfoRegistry
        """
        ...
    
    def getKeys(self, keys: List[bytes] ) -> None:
        """
        Cython signature: void getKeys(libcpp_vector[String] & keys)
        Fills the given vector with a list of all keys for which a value is set
        """
        ...
    
    def getMetaValue(self, in_0: Union[bytes, str, String] ) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getMetaValue(String)
        Returns the value corresponding to a string, or
        """
        ...
    
    def setMetaValue(self, in_0: Union[bytes, str, String] , in_1: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setMetaValue(String, DataValue)
        Sets the DataValue corresponding to a name
        """
        ...
    
    def metaValueExists(self, in_0: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool metaValueExists(String)
        Returns whether an entry with the given name exists
        """
        ...
    
    def removeMetaValue(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void removeMetaValue(String)
        Removes the DataValue corresponding to `name` if it exists
        """
        ...
    
    def __richcmp__(self, other: InstrumentSettings, op: int) -> Any:
        ... 


class InterpolationModel:
    """
    Cython implementation of _InterpolationModel

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1InterpolationModel.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void InterpolationModel()
        Abstract class for 1D-models that are approximated using linear interpolation
        """
        ...
    
    @overload
    def __init__(self, in_0: InterpolationModel ) -> None:
        """
        Cython signature: void InterpolationModel(InterpolationModel &)
        """
        ...
    
    def getIntensity(self, coord: float ) -> float:
        """
        Cython signature: double getIntensity(double coord)
        Access model predicted intensity at position 'pos'
        """
        ...
    
    def getScalingFactor(self) -> float:
        """
        Cython signature: double getScalingFactor()
        Returns the interpolation class
        """
        ...
    
    def setOffset(self, offset: float ) -> None:
        """
        Cython signature: void setOffset(double offset)
        Sets the offset of the model
        """
        ...
    
    def getCenter(self) -> float:
        """
        Cython signature: double getCenter()
        Returns the "center" of the model, particular definition (depends on the derived model)
        """
        ...
    
    def setSamples(self) -> None:
        """
        Cython signature: void setSamples()
        Sets sample/supporting points of interpolation wrt params
        """
        ...
    
    def setInterpolationStep(self, interpolation_step: float ) -> None:
        """
        Cython signature: void setInterpolationStep(double interpolation_step)
        Sets the interpolation step for the linear interpolation of the model
        """
        ...
    
    def setScalingFactor(self, scaling: float ) -> None:
        """
        Cython signature: void setScalingFactor(double scaling)
        Sets the scaling factor of the model
        """
        ...
    
    def getInterpolation(self) -> LinearInterpolation:
        """
        Cython signature: LinearInterpolation getInterpolation()
        Returns the interpolation class
        """
        ... 


class IonIdentityMolecularNetworking:
    """
    Cython implementation of _IonIdentityMolecularNetworking

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IonIdentityMolecularNetworking.html>`_

    Includes the necessary functions to generate filed required for GNPS ion identity molecular networking (IIMN).
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void IonIdentityMolecularNetworking()
        """
        ...
    
    annotateConsensusMap: __static_IonIdentityMolecularNetworking_annotateConsensusMap
    
    writeSupplementaryPairTable: __static_IonIdentityMolecularNetworking_writeSupplementaryPairTable 


class ItraqConstants:
    """
    Cython implementation of _ItraqConstants

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ItraqConstants.html>`_

    Some constants used throughout iTRAQ classes
    
    Constants for iTRAQ experiments and a ChannelInfo structure to store information about a single channel
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ItraqConstants()
        """
        ...
    
    @overload
    def __init__(self, in_0: ItraqConstants ) -> None:
        """
        Cython signature: void ItraqConstants(ItraqConstants &)
        """
        ...
    
    def getIsotopeMatrixAsStringList(self, itraq_type: int , isotope_corrections: List[MatrixDouble] ) -> List[bytes]:
        """
        Cython signature: StringList getIsotopeMatrixAsStringList(int itraq_type, libcpp_vector[MatrixDouble] & isotope_corrections)
        Convert isotope correction matrix to stringlist\n
        
        Each line is converted into a string of the format channel:-2Da/-1Da/+1Da/+2Da ; e.g. '114:0/0.3/4/0'
        Useful for creating parameters or debug output
        
        
        :param itraq_type: Which matrix to stringify. Should be of values from enum ITRAQ_TYPES
        :param isotope_corrections: Vector of the two matrices (4plex, 8plex)
        """
        ...
    
    def updateIsotopeMatrixFromStringList(self, itraq_type: int , channels: List[bytes] , isotope_corrections: List[MatrixDouble] ) -> None:
        """
        Cython signature: void updateIsotopeMatrixFromStringList(int itraq_type, StringList & channels, libcpp_vector[MatrixDouble] & isotope_corrections)
        Convert strings to isotope correction matrix rows\n
        
        Each string of format channel:-2Da/-1Da/+1Da/+2Da ; e.g. '114:0/0.3/4/0'
        is parsed and the corresponding channel(row) in the matrix is updated
        Not all channels need to be present, missing channels will be left untouched
        Useful to update the matrix with user isotope correction values
        
        
        :param itraq_type: Which matrix to stringify. Should be of values from enum ITRAQ_TYPES
        :param channels: New channel isotope values as strings
        :param isotope_corrections: Vector of the two matrices (4plex, 8plex)
        """
        ...
    
    def translateIsotopeMatrix(self, itraq_type: int , isotope_corrections: List[MatrixDouble] ) -> MatrixDouble:
        """
        Cython signature: MatrixDouble translateIsotopeMatrix(int & itraq_type, libcpp_vector[MatrixDouble] & isotope_corrections)
        """
        ... 


class JavaInfo:
    """
    Cython implementation of _JavaInfo

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1JavaInfo.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void JavaInfo()
        Detect Java and retrieve information
        """
        ...
    
    @overload
    def __init__(self, in_0: JavaInfo ) -> None:
        """
        Cython signature: void JavaInfo(JavaInfo &)
        """
        ...
    
    def canRun(self, java_executable: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool canRun(String java_executable)
        Determine if Java is installed and reachable\n
        
        The call fails if either Java is not installed or if a relative location is given and Java is not on the search PATH
        
        
        :param java_executable: Path to Java executable. Can be absolute, relative or just a filename
        :return: Returns false if Java executable can not be called; true if Java executable can be executed
        """
        ... 


class MRMFeatureFinderScoring:
    """
    Cython implementation of _MRMFeatureFinderScoring

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MRMFeatureFinderScoring.html>`_
      -- Inherits from ['DefaultParamHandler', 'ProgressLogger']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void MRMFeatureFinderScoring()
        """
        ...
    
    def pickExperiment(self, chromatograms: MSExperiment , output: FeatureMap , transition_exp_: TargetedExperiment , trafo: TransformationDescription , swath_map: MSExperiment ) -> None:
        """
        Cython signature: void pickExperiment(MSExperiment & chromatograms, FeatureMap & output, TargetedExperiment & transition_exp_, TransformationDescription trafo, MSExperiment & swath_map)
        Pick features in one experiment containing chromatogram
        
        Function for for wrapping in Python, only uses OpenMS datastructures and does not return the map
        
        
        :param chromatograms: The input chromatograms
        :param output: The output features with corresponding scores
        :param transition_exp: The transition list describing the experiment
        :param trafo: Optional transformation of the experimental retention time to the normalized retention time space used in the transition list
        :param swath_map: Optional SWATH-MS (DIA) map corresponding from which the chromatograms were extracted
        """
        ...
    
    def setStrictFlag(self, flag: bool ) -> None:
        """
        Cython signature: void setStrictFlag(bool flag)
        """
        ...
    
    @overload
    def setMS1Map(self, ms1_map: SpectrumAccessOpenMS ) -> None:
        """
        Cython signature: void setMS1Map(shared_ptr[SpectrumAccessOpenMS] ms1_map)
        """
        ...
    
    @overload
    def setMS1Map(self, ms1_map: SpectrumAccessOpenMSCached ) -> None:
        """
        Cython signature: void setMS1Map(shared_ptr[SpectrumAccessOpenMSCached] ms1_map)
        """
        ...
    
    def scorePeakgroups(self, transition_group: LightMRMTransitionGroupCP , trafo: TransformationDescription , swath_maps: List[SwathMap] , output: FeatureMap , ms1only: bool ) -> None:
        """
        Cython signature: void scorePeakgroups(LightMRMTransitionGroupCP transition_group, TransformationDescription trafo, libcpp_vector[SwathMap] swath_maps, FeatureMap & output, bool ms1only)
        Score all peak groups of a transition group
        
        Iterate through all features found along the chromatograms of the transition group and score each one individually
        
        
        :param transition_group: The MRMTransitionGroup to be scored (input)
        :param trafo: Optional transformation of the experimental retention time
            to the normalized retention time space used in thetransition list
        :param swath_maps: Optional SWATH-MS (DIA) map corresponding from which
            the chromatograms were extracted. Use empty map if no data is available
        :param output: The output features with corresponding scores (the found
            features will be added to this FeatureMap)
        :param ms1only: Whether to only do MS1 scoring and skip all MS2 scoring
        """
        ...
    
    def prepareProteinPeptideMaps_(self, transition_exp: LightTargetedExperiment ) -> None:
        """
        Cython signature: void prepareProteinPeptideMaps_(LightTargetedExperiment & transition_exp)
        Prepares the internal mappings of peptides and proteins
        
        Calling this method _is_ required before calling scorePeakgroups
        
        
        :param transition_exp: The transition list describing the experiment
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ...
    
    def setLogType(self, in_0: int ) -> None:
        """
        Cython signature: void setLogType(LogType)
        Sets the progress log that should be used. The default type is NONE!
        """
        ...
    
    def getLogType(self) -> int:
        """
        Cython signature: LogType getLogType()
        Returns the type of progress log being used
        """
        ...
    
    def startProgress(self, begin: int , end: int , label: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void startProgress(ptrdiff_t begin, ptrdiff_t end, String label)
        """
        ...
    
    def setProgress(self, value: int ) -> None:
        """
        Cython signature: void setProgress(ptrdiff_t value)
        Sets the current progress
        """
        ...
    
    def endProgress(self) -> None:
        """
        Cython signature: void endProgress()
        Ends the progress display
        """
        ...
    
    def nextProgress(self) -> None:
        """
        Cython signature: void nextProgress()
        Increment progress by 1 (according to range begin-end)
        """
        ... 


class MRMFragmentSelection:
    """
    Cython implementation of _MRMFragmentSelection

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MRMFragmentSelection.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MRMFragmentSelection()
        """
        ...
    
    @overload
    def __init__(self, in_0: MRMFragmentSelection ) -> None:
        """
        Cython signature: void MRMFragmentSelection(MRMFragmentSelection &)
        """
        ...
    
    def selectFragments(self, selected_peaks: List[Peak1D] , spec: MSSpectrum ) -> None:
        """
        Cython signature: void selectFragments(libcpp_vector[Peak1D] & selected_peaks, MSSpectrum & spec)
        Selects accordingly to the parameters the best peaks of spec and writes them into `selected_peaks`
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class MRMRTNormalizer:
    """
    Cython implementation of _MRMRTNormalizer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MRMRTNormalizer.html>`_
    """
    
    chauvenet: __static_MRMRTNormalizer_chauvenet
    
    chauvenet_probability: __static_MRMRTNormalizer_chauvenet_probability
    
    computeBinnedCoverage: __static_MRMRTNormalizer_computeBinnedCoverage
    
    removeOutliersIterative: __static_MRMRTNormalizer_removeOutliersIterative
    
    removeOutliersRANSAC: __static_MRMRTNormalizer_removeOutliersRANSAC 


class MRMTransitionGroupPicker:
    """
    Cython implementation of _MRMTransitionGroupPicker

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MRMTransitionGroupPicker.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MRMTransitionGroupPicker()
        """
        ...
    
    @overload
    def __init__(self, in_0: MRMTransitionGroupPicker ) -> None:
        """
        Cython signature: void MRMTransitionGroupPicker(MRMTransitionGroupPicker &)
        """
        ...
    
    @overload
    def pickTransitionGroup(self, transition_group: LightMRMTransitionGroupCP ) -> None:
        """
        Cython signature: void pickTransitionGroup(LightMRMTransitionGroupCP transition_group)
        """
        ...
    
    @overload
    def pickTransitionGroup(self, transition_group: MRMTransitionGroupCP ) -> None:
        """
        Cython signature: void pickTransitionGroup(MRMTransitionGroupCP transition_group)
        """
        ...
    
    def createMRMFeature(self, transition_group: LightMRMTransitionGroupCP , picked_chroms: List[MSChromatogram] , smoothed_chroms: List[MSChromatogram] , chr_idx: int , peak_idx: int ) -> MRMFeature:
        """
        Cython signature: MRMFeature createMRMFeature(LightMRMTransitionGroupCP transition_group, libcpp_vector[MSChromatogram] & picked_chroms, libcpp_vector[MSChromatogram] & smoothed_chroms, const int chr_idx, const int peak_idx)
        """
        ...
    
    def remove_overlapping_features(self, picked_chroms: List[MSChromatogram] , best_left: float , best_right: float ) -> None:
        """
        Cython signature: void remove_overlapping_features(libcpp_vector[MSChromatogram] & picked_chroms, double best_left, double best_right)
        """
        ...
    
    def findLargestPeak(self, picked_chroms: List[MSChromatogram] , chr_idx: int , peak_idx: int ) -> None:
        """
        Cython signature: void findLargestPeak(libcpp_vector[MSChromatogram] & picked_chroms, int & chr_idx, int & peak_idx)
        """
        ...
    
    def findWidestPeakIndices(self, picked_chroms: List[MSChromatogram] , chrom_idx: int , point_idx: int ) -> None:
        """
        Cython signature: void findWidestPeakIndices(libcpp_vector[MSChromatogram] & picked_chroms, int & chrom_idx, int & point_idx)
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class MapAlignmentAlgorithmKD:
    """
    Cython implementation of _MapAlignmentAlgorithmKD

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MapAlignmentAlgorithmKD.html>`_

    An efficient reference-free feature map alignment algorithm for unlabeled data
    
    This algorithm uses a kd-tree to efficiently compute conflict-free connected components (CCC)
    in a compatibility graph on feature data. This graph is comprised of nodes corresponding
    to features and edges connecting features f and f' iff both are within each other's tolerance
    windows (wrt. RT and m/z difference). CCCs are those CCs that do not contain multiple features
    from the same input map, and whose features all have the same charge state
    
    All CCCs above a user-specified minimum size are considered true sets of corresponding features
    and based on these, LOWESS transformations are computed for each input map such that the average
    deviation from the mean retention time within all CCCs is minimized
    """
    
    @overload
    def __init__(self, num_maps: int , param: Param ) -> None:
        """
        Cython signature: void MapAlignmentAlgorithmKD(size_t num_maps, Param & param)
        """
        ...
    
    @overload
    def __init__(self, in_0: MapAlignmentAlgorithmKD ) -> None:
        """
        Cython signature: void MapAlignmentAlgorithmKD(MapAlignmentAlgorithmKD &)
        """
        ...
    
    def addRTFitData(self, kd_data: KDTreeFeatureMaps ) -> None:
        """
        Cython signature: void addRTFitData(KDTreeFeatureMaps & kd_data)
        Compute data points needed for RT transformation in the current `kd_data`, add to `fit_data_`
        """
        ...
    
    def fitLOWESS(self) -> None:
        """
        Cython signature: void fitLOWESS()
        Fit LOWESS to fit_data_, store final models in `transformations_`
        """
        ...
    
    def transform(self, kd_data: KDTreeFeatureMaps ) -> None:
        """
        Cython signature: void transform(KDTreeFeatureMaps & kd_data)
        Transform RTs for `kd_data`
        """
        ... 


class MascotInfile:
    """
    Cython implementation of _MascotInfile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MascotInfile.html>`_
      -- Inherits from ['ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MascotInfile()
        """
        ...
    
    @overload
    def __init__(self, in_0: MascotInfile ) -> None:
        """
        Cython signature: void MascotInfile(MascotInfile &)
        """
        ...
    
    @overload
    def store(self, filename: Union[bytes, str, String] , spec: MSSpectrum , mz: float , retention_time: float , search_title: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void store(const String & filename, MSSpectrum & spec, double mz, double retention_time, String search_title)
        Stores the peak list in a MascotInfile that can be used as input for MASCOT shell execution
        """
        ...
    
    @overload
    def store(self, filename: Union[bytes, str, String] , experiment: MSExperiment , search_title: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void store(const String & filename, MSExperiment & experiment, String search_title)
        Stores the experiment data in a MascotInfile that can be used as input for MASCOT shell execution
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , exp: MSExperiment ) -> None:
        """
        Cython signature: void load(const String & filename, MSExperiment & exp)
        Loads a Mascot Generic File into a PeakMap
        
        
        :param filename: File name which the map should be read from
        :param exp: The map which is filled with the data from the given file
        :raises:
          Exception: FileNotFound is thrown if the given file could not be found
        """
        ...
    
    def getBoundary(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getBoundary()
        Returns the boundary used for the MIME format
        """
        ...
    
    def setBoundary(self, boundary: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setBoundary(const String & boundary)
        Sets the boundary used for the MIME format.By default a 22 character random string is used
        """
        ...
    
    def getDB(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getDB()
        Returns the DB to use
        """
        ...
    
    def setDB(self, db: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setDB(const String & db)
        Sets the DB (default MSDB). See mascot path /config/mascot.dat in "Databases" section for possible settings
        """
        ...
    
    def getSearchType(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getSearchType()
        Returns the search type
        """
        ...
    
    def setSearchType(self, search_type: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setSearchType(const String & search_type)
        Sets the search type (default MIS). So far only MIS is supported!Valid types are "MIS" (MS/MS Ion Search), "PMF" (Peptide Mass Fingerprint) , "SQ" (Sequence Query)
        """
        ...
    
    def getHits(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getHits()
        Returns the number of hits to report back
        """
        ...
    
    def setHits(self, hits: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setHits(const String & hits)
        Sets the number of hits to report back (default 20)
        """
        ...
    
    def getCleavage(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCleavage()
        Returns the enzyme used for cleavage
        """
        ...
    
    def setCleavage(self, cleavage: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCleavage(const String & cleavage)
        Sets the enzyme used for cleavage (default Trypsin). See mascot path /config/enzymes for possible settings
        """
        ...
    
    def getMassType(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getMassType()
        Returns the used mass type ("Monoisotopic" or "Average")
        """
        ...
    
    def setMassType(self, mass_type: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setMassType(const String & mass_type)
        Sets the used mass type "Monoisotopic" or "Average" (default Monoisotopic)
        """
        ...
    
    def getModifications(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getModifications()
        Returns a vector containing the fixed modifications (default none)
        """
        ...
    
    def setModifications(self, mods: List[bytes] ) -> None:
        """
        Cython signature: void setModifications(libcpp_vector[String] & mods)
        Sets the fixed modifications (default none). See mascot path /config/mod_file for possible settings
        """
        ...
    
    def getVariableModifications(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getVariableModifications()
        Returns a vector containing the variable modifications (default none)
        """
        ...
    
    def setVariableModifications(self, mods: List[bytes] ) -> None:
        """
        Cython signature: void setVariableModifications(libcpp_vector[String] & mods)
        Sets the fixed modifications (default none). See mascot path /config/mod_file for possible settings
        """
        ...
    
    def getInstrument(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getInstrument()
        Returns the instrument type
        """
        ...
    
    def setInstrument(self, instrument: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setInstrument(const String & instrument)
        Sets the instrument type (Default Default). Possible instruments are ESI-QUAD-TOF, MALDI-TOF-PSD, ESI-TRAP, ESI-QUAD, ESI-FTICR, MALDI-TOF-TOF, ESI-4SECTOR, FTMS-ECD, MALDI-QUAD-TOF, MALDI-QIT-TOF
        """
        ...
    
    def getMissedCleavages(self) -> int:
        """
        Cython signature: unsigned int getMissedCleavages()
        Returns the number of allowed missed cleavages
        """
        ...
    
    def setMissedCleavages(self, missed_cleavages: int ) -> None:
        """
        Cython signature: void setMissedCleavages(unsigned int missed_cleavages)
        Sets the number of allowed missed cleavages (default 1)
        """
        ...
    
    def getPrecursorMassTolerance(self) -> float:
        """
        Cython signature: float getPrecursorMassTolerance()
        Returns the precursor mass tolerance
        """
        ...
    
    def setPrecursorMassTolerance(self, precursor_mass_tolerance: float ) -> None:
        """
        Cython signature: void setPrecursorMassTolerance(float precursor_mass_tolerance)
        Sets the precursor mass tolerance in Da (default 2.0)
        """
        ...
    
    def getPeakMassTolerance(self) -> float:
        """
        Cython signature: float getPeakMassTolerance()
        Returns the peak mass tolerance in Da
        """
        ...
    
    def setPeakMassTolerance(self, ion_mass_tolerance: float ) -> None:
        """
        Cython signature: void setPeakMassTolerance(float ion_mass_tolerance)
        Sets the peak mass tolerance in Da (default 1.0)
        """
        ...
    
    def getTaxonomy(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getTaxonomy()
        Returns the taxonomy
        """
        ...
    
    def setTaxonomy(self, taxonomy: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setTaxonomy(const String & taxonomy)
        Sets the taxonomy (default All entries). See mascot path /config/taxonomy for possible settings
        """
        ...
    
    def getFormVersion(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getFormVersion()
        Returns the Mascot form version
        """
        ...
    
    def setFormVersion(self, form_version: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setFormVersion(const String & form_version)
        Sets the Mascot form version (default 1.01)
        """
        ...
    
    def getCharges(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCharges()
        Returns the charges
        """
        ...
    
    def setCharges(self, charges: List[int] ) -> None:
        """
        Cython signature: void setCharges(libcpp_vector[int] & charges)
        Sets the charges (default 1+, 2+ and 3+)
        """
        ...
    
    def setLogType(self, in_0: int ) -> None:
        """
        Cython signature: void setLogType(LogType)
        Sets the progress log that should be used. The default type is NONE!
        """
        ...
    
    def getLogType(self) -> int:
        """
        Cython signature: LogType getLogType()
        Returns the type of progress log being used
        """
        ...
    
    def startProgress(self, begin: int , end: int , label: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void startProgress(ptrdiff_t begin, ptrdiff_t end, String label)
        """
        ...
    
    def setProgress(self, value: int ) -> None:
        """
        Cython signature: void setProgress(ptrdiff_t value)
        Sets the current progress
        """
        ...
    
    def endProgress(self) -> None:
        """
        Cython signature: void endProgress()
        Ends the progress display
        """
        ...
    
    def nextProgress(self) -> None:
        """
        Cython signature: void nextProgress()
        Increment progress by 1 (according to range begin-end)
        """
        ... 


class MassDecomposition:
    """
    Cython implementation of _MassDecomposition

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MassDecomposition.html>`_

    Class represents a decomposition of a mass into amino acids
    
    This class represents a mass decomposition into amino acids. A
    decomposition are amino acids given with frequencies which add
    up to a specific mass.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MassDecomposition()
        """
        ...
    
    @overload
    def __init__(self, in_0: MassDecomposition ) -> None:
        """
        Cython signature: void MassDecomposition(MassDecomposition &)
        """
        ...
    
    @overload
    def __init__(self, deco: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void MassDecomposition(const String & deco)
        """
        ...
    
    def toString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        Returns the decomposition as a string
        """
        ...
    
    def toExpandedString(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toExpandedString()
        Returns the decomposition as a string; instead of frequencies the amino acids are repeated
        """
        ...
    
    def getNumberOfMaxAA(self) -> int:
        """
        Cython signature: size_t getNumberOfMaxAA()
        Returns the max frequency of this composition
        """
        ...
    
    def containsTag(self, tag: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool containsTag(const String & tag)
        Returns true if tag is contained in the mass decomposition
        """
        ...
    
    def compatible(self, deco: MassDecomposition ) -> bool:
        """
        Cython signature: bool compatible(MassDecomposition & deco)
        Returns true if the mass decomposition if contained in this instance
        """
        ...
    
    def __str__(self) -> Union[bytes, str, String]:
        """
        Cython signature: String toString()
        Returns the decomposition as a string
        """
        ... 


class MorpheusScore:
    """
    Cython implementation of _MorpheusScore

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MorpheusScore.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MorpheusScore()
        """
        ...
    
    @overload
    def __init__(self, in_0: MorpheusScore ) -> None:
        """
        Cython signature: void MorpheusScore(MorpheusScore &)
        """
        ...
    
    def compute(self, fragment_mass_tolerance: float , fragment_mass_tolerance_unit_ppm: bool , exp_spectrum: MSSpectrum , theo_spectrum: MSSpectrum ) -> MorpheusScore_Result:
        """
        Cython signature: MorpheusScore_Result compute(double fragment_mass_tolerance, bool fragment_mass_tolerance_unit_ppm, const MSSpectrum & exp_spectrum, const MSSpectrum & theo_spectrum)
        Returns Morpheus Score
        """
        ... 


class MorpheusScore_Result:
    """
    Cython implementation of _MorpheusScore_Result

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MorpheusScore_Result.html>`_
    """
    
    matches: int
    
    n_peaks: int
    
    score: float
    
    MIC: float
    
    TIC: float
    
    err: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MorpheusScore_Result()
        """
        ...
    
    @overload
    def __init__(self, in_0: MorpheusScore_Result ) -> None:
        """
        Cython signature: void MorpheusScore_Result(MorpheusScore_Result &)
        """
        ... 


class MzDataFile:
    """
    Cython implementation of _MzDataFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MzDataFile.html>`_
      -- Inherits from ['ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MzDataFile()
        File adapter for MzData files
        """
        ...
    
    @overload
    def __init__(self, in_0: MzDataFile ) -> None:
        """
        Cython signature: void MzDataFile(MzDataFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , map: MSExperiment ) -> None:
        """
        Cython signature: void load(const String & filename, MSExperiment & map)
        Loads a map from a MzData file
        
        
        :param filename: Directory of the file with the file name
        :param map: It has to be a MSExperiment or have the same interface
        :raises:
          Exception: FileNotFound is thrown if the file could not be opened
        :raises:
          Exception: ParseError is thrown if an error occurs during parsing
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , map: MSExperiment ) -> None:
        """
        Cython signature: void store(const String & filename, MSExperiment & map)
        Stores a map in a MzData file
        
        
        :param filename: Directory of the file with the file name
        :param map: It has to be a MSExperiment or have the same interface
        :raises:
          Exception: UnableToCreateFile is thrown if the file could not be created
        """
        ...
    
    def getOptions(self) -> PeakFileOptions:
        """
        Cython signature: PeakFileOptions getOptions()
        Returns the options for loading/storing
        """
        ...
    
    def setOptions(self, in_0: PeakFileOptions ) -> None:
        """
        Cython signature: void setOptions(PeakFileOptions)
        Sets options for loading/storing
        """
        ...
    
    def isSemanticallyValid(self, filename: Union[bytes, str, String] , errors: List[bytes] , warnings: List[bytes] ) -> bool:
        """
        Cython signature: bool isSemanticallyValid(const String & filename, StringList & errors, StringList & warnings)
        Checks if a file is valid with respect to the mapping file and the controlled vocabulary
        
        
        :param filename: File name of the file to be checked
        :param errors: Errors during the validation are returned in this output parameter
        :param warnings: Warnings during the validation are returned in this output parameter
        :raises:
          Exception: FileNotFound is thrown if the file could not be opened
        """
        ...
    
    def setLogType(self, in_0: int ) -> None:
        """
        Cython signature: void setLogType(LogType)
        Sets the progress log that should be used. The default type is NONE!
        """
        ...
    
    def getLogType(self) -> int:
        """
        Cython signature: LogType getLogType()
        Returns the type of progress log being used
        """
        ...
    
    def startProgress(self, begin: int , end: int , label: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void startProgress(ptrdiff_t begin, ptrdiff_t end, String label)
        """
        ...
    
    def setProgress(self, value: int ) -> None:
        """
        Cython signature: void setProgress(ptrdiff_t value)
        Sets the current progress
        """
        ...
    
    def endProgress(self) -> None:
        """
        Cython signature: void endProgress()
        Ends the progress display
        """
        ...
    
    def nextProgress(self) -> None:
        """
        Cython signature: void nextProgress()
        Increment progress by 1 (according to range begin-end)
        """
        ... 


class MzMLFile:
    """
    Cython implementation of _MzMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MzMLFile.html>`_
      -- Inherits from ['ProgressLogger']

    File adapter for MzML files
    
    Provides methods to load and store MzML files.
    PeakFileOptions allow to load a reduced subset of the data into an MSExperiment.
    
    See help(MSExperiment) how data is stored after loading.
    See help(PeakFileOptions) for available options.
    
    Usage:
    
    .. code-block:: python
    
      exp = MSExperiment()
      MzMLFile().load("test.mzML", exp)
      spec = []
      for s in exp.getSpectra():
        if s.getMSLevel() != 1:
          spec.append(s)
      exp.setSpectra(spec)
      MzMLFile().store("filtered.mzML", exp)
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MzMLFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: MzMLFile ) -> None:
        """
        Cython signature: void MzMLFile(MzMLFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , in_1: MSExperiment ) -> None:
        """
        Cython signature: void load(const String & filename, MSExperiment &)
        Loads from an MzML file. Spectra and chromatograms are sorted by default (this can be disabled using PeakFileOptions)
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , in_1: MSExperiment ) -> None:
        """
        Cython signature: void store(const String & filename, MSExperiment &)
        Stores a MSExperiment in an MzML file
        """
        ...
    
    def storeBuffer(self, output: String , exp: MSExperiment ) -> None:
        """
        Cython signature: void storeBuffer(String & output, MSExperiment exp)
        Stores a map in an output string
        
        
        :param output: An empty string to store the result
        :param exp: Has to be an MSExperiment
        """
        ...
    
    def loadBuffer(self, input: Union[bytes, str, String] , exp: MSExperiment ) -> None:
        """
        Cython signature: void loadBuffer(const String & input, MSExperiment & exp)
        Loads a map from a MzML file stored in a buffer (in memory)
        
        
        :param buffer: The buffer with the data (i.e. string with content of an mzML file)
        :param exp: Is an MSExperiment
        :raises:
          Exception: ParseError is thrown if an error occurs during parsing
        """
        ...
    
    def getOptions(self) -> PeakFileOptions:
        """
        Cython signature: PeakFileOptions getOptions()
        """
        ...
    
    def setOptions(self, in_0: PeakFileOptions ) -> None:
        """
        Cython signature: void setOptions(PeakFileOptions)
        Set PeakFileOptions to perform filtering during loading. E.g., to load only MS1 spectra or meta data only
        """
        ...
    
    def isSemanticallyValid(self, filename: Union[bytes, str, String] , errors: List[bytes] , warnings: List[bytes] ) -> bool:
        """
        Cython signature: bool isSemanticallyValid(const String & filename, StringList & errors, StringList & warnings)
        """
        ...
    
    def setLogType(self, in_0: int ) -> None:
        """
        Cython signature: void setLogType(LogType)
        Sets the progress log that should be used. The default type is NONE!
        """
        ...
    
    def getLogType(self) -> int:
        """
        Cython signature: LogType getLogType()
        Returns the type of progress log being used
        """
        ...
    
    def startProgress(self, begin: int , end: int , label: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void startProgress(ptrdiff_t begin, ptrdiff_t end, String label)
        """
        ...
    
    def setProgress(self, value: int ) -> None:
        """
        Cython signature: void setProgress(ptrdiff_t value)
        Sets the current progress
        """
        ...
    
    def endProgress(self) -> None:
        """
        Cython signature: void endProgress()
        Ends the progress display
        """
        ...
    
    def nextProgress(self) -> None:
        """
        Cython signature: void nextProgress()
        Increment progress by 1 (according to range begin-end)
        """
        ... 


class MzMLSqliteHandler:
    """
    Cython implementation of _MzMLSqliteHandler

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Internal_1_1MzMLSqliteHandler.html>`_
    """
    
    @overload
    def __init__(self, filename: Union[bytes, str, String] , run_id: int ) -> None:
        """
        Cython signature: void MzMLSqliteHandler(String filename, uint64_t run_id)
        """
        ...
    
    @overload
    def __init__(self, in_0: MzMLSqliteHandler ) -> None:
        """
        Cython signature: void MzMLSqliteHandler(MzMLSqliteHandler &)
        """
        ...
    
    def readExperiment(self, exp: MSExperiment , meta_only: bool ) -> None:
        """
        Cython signature: void readExperiment(MSExperiment & exp, bool meta_only)
        Read an experiment into an MSExperiment structure
        
        
        :param exp: The result data structure
        :param meta_only: Only read the meta data
        """
        ...
    
    def readSpectra(self, exp: List[MSSpectrum] , indices: List[int] , meta_only: bool ) -> None:
        """
        Cython signature: void readSpectra(libcpp_vector[MSSpectrum] & exp, libcpp_vector[int] indices, bool meta_only)
        Read a set of spectra (potentially restricted to a subset)
        
        
        :param exp: The result data structure
        :param indices: A list of indices restricting the resulting spectra only to those specified here
        :param meta_only: Only read the meta data
        """
        ...
    
    def readChromatograms(self, exp: List[MSChromatogram] , indices: List[int] , meta_only: bool ) -> None:
        """
        Cython signature: void readChromatograms(libcpp_vector[MSChromatogram] & exp, libcpp_vector[int] indices, bool meta_only)
        Read a set of chromatograms (potentially restricted to a subset)
        
        
        :param exp: The result data structure
        :param indices: A list of indices restricting the resulting spectra only to those specified here
        :param meta_only: Only read the meta data
        """
        ...
    
    def getNrSpectra(self) -> int:
        """
        Cython signature: size_t getNrSpectra()
        Returns number of spectra in the file, reutrns the number of spectra
        """
        ...
    
    def getNrChromatograms(self) -> int:
        """
        Cython signature: size_t getNrChromatograms()
        Returns the number of chromatograms in the file
        """
        ...
    
    def setConfig(self, write_full_meta: bool , use_lossy_compression: bool , linear_abs_mass_acc: float ) -> None:
        """
        Cython signature: void setConfig(bool write_full_meta, bool use_lossy_compression, double linear_abs_mass_acc)
        Sets file configuration
        
        
        :param write_full_meta: Whether to write a complete mzML meta data structure into the RUN_EXTRA field (allows complete recovery of the input file)
        :param use_lossy_compression: Whether to use lossy compression (ms numpress)
        :param linear_abs_mass_acc: Accepted loss in mass accuracy (absolute m/z, in Th)
        """
        ...
    
    def getSpectraIndicesbyRT(self, RT: float , deltaRT: float , indices: List[int] ) -> List[int]:
        """
        Cython signature: libcpp_vector[size_t] getSpectraIndicesbyRT(double RT, double deltaRT, libcpp_vector[int] indices)
        Returns spectral indices around a specific retention time
        
        :param RT: The retention time
        :param deltaRT: Tolerance window around RT (if less or equal than zero, only the first spectrum *after* RT is returned)
        :param indices: Spectra to consider (if empty, all spectra are considered)
        :return: The indices of the spectra within RT +/- deltaRT
        """
        ...
    
    def writeExperiment(self, exp: MSExperiment ) -> None:
        """
        Cython signature: void writeExperiment(MSExperiment exp)
        Write an MSExperiment to disk
        """
        ...
    
    def createTables(self) -> None:
        """
        Cython signature: void createTables()
        Create data tables for a new file
        """
        ...
    
    def writeSpectra(self, spectra: List[MSSpectrum] ) -> None:
        """
        Cython signature: void writeSpectra(libcpp_vector[MSSpectrum] spectra)
        Writes a set of spectra to disk
        """
        ...
    
    def writeChromatograms(self, chroms: List[MSChromatogram] ) -> None:
        """
        Cython signature: void writeChromatograms(libcpp_vector[MSChromatogram] chroms)
        Writes a set of chromatograms to disk
        """
        ...
    
    def writeRunLevelInformation(self, exp: MSExperiment , write_full_meta: bool ) -> None:
        """
        Cython signature: void writeRunLevelInformation(MSExperiment exp, bool write_full_meta)
        Write the run-level information for an experiment into tables
        
        This is a low level function, do not call this function unless you know what you are doing
        
        
        :param exp: The result data structure
        :param meta_only: Only read the meta data
        """
        ...
    
    def getRunID(self) -> int:
        """
        Cython signature: uint64_t getRunID()
        Extract the `RUN` ID from the sqMass file
        """
        ... 


class MzTabFile:
    """
    Cython implementation of _MzTabFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MzTabFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MzTabFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: MzTabFile ) -> None:
        """
        Cython signature: void MzTabFile(MzTabFile &)
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , mz_tab: MzTab ) -> None:
        """
        Cython signature: void store(String filename, MzTab & mz_tab)
        Stores MzTab file
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , mz_tab: MzTab ) -> None:
        """
        Cython signature: void load(String filename, MzTab & mz_tab)
        Loads MzTab file
        """
        ... 


class NLargest:
    """
    Cython implementation of _NLargest

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1NLargest.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void NLargest()
        """
        ...
    
    @overload
    def __init__(self, in_0: NLargest ) -> None:
        """
        Cython signature: void NLargest(NLargest &)
        """
        ...
    
    def filterSpectrum(self, spec: MSSpectrum ) -> None:
        """
        Cython signature: void filterSpectrum(MSSpectrum & spec)
        Keep only n-largest peaks in spectrum
        """
        ...
    
    def filterPeakSpectrum(self, spec: MSSpectrum ) -> None:
        """
        Cython signature: void filterPeakSpectrum(MSSpectrum & spec)
        Keep only n-largest peaks in spectrum
        """
        ...
    
    def filterPeakMap(self, exp: MSExperiment ) -> None:
        """
        Cython signature: void filterPeakMap(MSExperiment & exp)
        Keep only n-largest peaks in each spectrum of a peak map
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class OMSSACSVFile:
    """
    Cython implementation of _OMSSACSVFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OMSSACSVFile.html>`_

    File adapter for OMSSACSV files
    
    The files contain the results of the OMSSA algorithm in a comma separated manner. This file adapter is able to
    load the data from such a file into the structures of OpenMS
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OMSSACSVFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: OMSSACSVFile ) -> None:
        """
        Cython signature: void OMSSACSVFile(OMSSACSVFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , protein_identification: ProteinIdentification , id_data: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void load(const String & filename, ProteinIdentification & protein_identification, libcpp_vector[PeptideIdentification] & id_data)
        Loads a OMSSA file
        
        The content of the file is stored in `features`
        
        
        :param filename: The name of the file to read from
        :param protein_identification: The protein ProteinIdentification data
        :param id_data: The peptide ids of the file
        :raises:
          Exception: FileNotFound is thrown if the file could not be opened
        :raises:
          Exception: ParseError is thrown if an error occurs during parsing
        """
        ... 


class OSBinaryDataArray:
    """
    Cython implementation of _OSBinaryDataArray

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1OSBinaryDataArray.html>`_
    """
    
    data: List[float]
    
    description: bytes
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OSBinaryDataArray()
        """
        ...
    
    @overload
    def __init__(self, in_0: OSBinaryDataArray ) -> None:
        """
        Cython signature: void OSBinaryDataArray(OSBinaryDataArray &)
        """
        ... 


class OSChromatogram:
    """
    Cython implementation of _OSChromatogram

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1OSChromatogram.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OSChromatogram()
        """
        ...
    
    @overload
    def __init__(self, in_0: OSChromatogram ) -> None:
        """
        Cython signature: void OSChromatogram(OSChromatogram &)
        """
        ... 


class OSSpectrum:
    """
    Cython implementation of _OSSpectrum

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1OSSpectrum.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OSSpectrum()
        """
        ...
    
    @overload
    def __init__(self, in_0: OSSpectrum ) -> None:
        """
        Cython signature: void OSSpectrum(OSSpectrum &)
        """
        ... 


class OpenSwathScoring:
    """
    Cython implementation of _OpenSwathScoring

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OpenSwathScoring.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OpenSwathScoring()
        """
        ...
    
    @overload
    def __init__(self, in_0: OpenSwathScoring ) -> None:
        """
        Cython signature: void OpenSwathScoring(OpenSwathScoring &)
        """
        ...
    
    def initialize(self, rt_normalization_factor: float , add_up_spectra: int , spacing_for_spectra_resampling: float , drift_extra: float , su: OpenSwath_Scores_Usage , spectrum_addition_method: bytes ) -> None:
        """
        Cython signature: void initialize(double rt_normalization_factor, int add_up_spectra, double spacing_for_spectra_resampling, double drift_extra, OpenSwath_Scores_Usage su, libcpp_string spectrum_addition_method)
        Initialize the scoring object\n
        Sets the parameters for the scoring
        
        
        :param rt_normalization_factor: Specifies the range of the normalized retention time space
        :param add_up_spectra: How many spectra to add up (default 1)
        :param spacing_for_spectra_resampling: Spacing factor for spectra addition
        :param su: Which scores to actually compute
        :param spectrum_addition_method: Method to use for spectrum addition (valid: "simple", "resample")
        """
        ...
    
    def getNormalized_library_intensities_(self, transitions: List[LightTransition] , normalized_library_intensity: List[float] ) -> None:
        """
        Cython signature: void getNormalized_library_intensities_(libcpp_vector[LightTransition] transitions, libcpp_vector[double] normalized_library_intensity)
        """
        ... 


class OpenSwath_Scores:
    """
    Cython implementation of _OpenSwath_Scores

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OpenSwath_Scores.html>`_
    """
    
    elution_model_fit_score: float
    
    library_corr: float
    
    library_norm_manhattan: float
    
    library_rootmeansquare: float
    
    library_sangle: float
    
    norm_rt_score: float
    
    isotope_correlation: float
    
    isotope_overlap: float
    
    massdev_score: float
    
    xcorr_coelution_score: float
    
    xcorr_shape_score: float
    
    yseries_score: float
    
    bseries_score: float
    
    log_sn_score: float
    
    weighted_coelution_score: float
    
    weighted_xcorr_shape: float
    
    weighted_massdev_score: float
    
    ms1_xcorr_coelution_score: float
    
    ms1_xcorr_coelution_contrast_score: float
    
    ms1_xcorr_coelution_combined_score: float
    
    ms1_xcorr_shape_score: float
    
    ms1_xcorr_shape_contrast_score: float
    
    ms1_xcorr_shape_combined_score: float
    
    ms1_ppm_score: float
    
    ms1_isotope_correlation: float
    
    ms1_isotope_overlap: float
    
    ms1_mi_score: float
    
    ms1_mi_contrast_score: float
    
    ms1_mi_combined_score: float
    
    sonar_sn: float
    
    sonar_diff: float
    
    sonar_trend: float
    
    sonar_rsq: float
    
    sonar_shape: float
    
    sonar_lag: float
    
    library_manhattan: float
    
    library_dotprod: float
    
    intensity: float
    
    total_xic: float
    
    nr_peaks: float
    
    sn_ratio: float
    
    mi_score: float
    
    weighted_mi_score: float
    
    rt_difference: float
    
    normalized_experimental_rt: float
    
    raw_rt_score: float
    
    dotprod_score_dia: float
    
    manhatt_score_dia: float
    
    def __init__(self) -> None:
        """
        Cython signature: void OpenSwath_Scores()
        """
        ...
    
    def get_quick_lda_score(self, library_corr_: float , library_norm_manhattan_: float , norm_rt_score_: float , xcorr_coelution_score_: float , xcorr_shape_score_: float , log_sn_score_: float ) -> float:
        """
        Cython signature: double get_quick_lda_score(double library_corr_, double library_norm_manhattan_, double norm_rt_score_, double xcorr_coelution_score_, double xcorr_shape_score_, double log_sn_score_)
        """
        ...
    
    def calculate_lda_prescore(self, scores: OpenSwath_Scores ) -> float:
        """
        Cython signature: double calculate_lda_prescore(OpenSwath_Scores scores)
        """
        ...
    
    def calculate_swath_lda_prescore(self, scores: OpenSwath_Scores ) -> float:
        """
        Cython signature: double calculate_swath_lda_prescore(OpenSwath_Scores scores)
        """
        ... 


class OpenSwath_Scores_Usage:
    """
    Cython implementation of _OpenSwath_Scores_Usage

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OpenSwath_Scores_Usage.html>`_
    """
    
    use_coelution_score_: bool
    
    use_shape_score_: bool
    
    use_rt_score_: bool
    
    use_library_score_: bool
    
    use_elution_model_score_: bool
    
    use_intensity_score_: bool
    
    use_total_xic_score_: bool
    
    use_total_mi_score_: bool
    
    use_nr_peaks_score_: bool
    
    use_sn_score_: bool
    
    use_mi_score_: bool
    
    use_dia_scores_: bool
    
    use_sonar_scores: bool
    
    use_ms1_correlation: bool
    
    use_ms1_fullscan: bool
    
    use_ms1_mi: bool
    
    use_uis_scores: bool
    
    def __init__(self) -> None:
        """
        Cython signature: void OpenSwath_Scores_Usage()
        """
        ... 


class OptimizationFunctions_PenaltyFactors:
    """
    Cython implementation of _OptimizationFunctions_PenaltyFactors

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OptimizationFunctions_PenaltyFactors.html>`_
    """
    
    pos: float
    
    lWidth: float
    
    rWidth: float
    
    def __init__(self) -> None:
        """
        Cython signature: void OptimizationFunctions_PenaltyFactors()
        """
        ... 


class OptimizePick:
    """
    Cython implementation of _OptimizePick

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OptimizePick.html>`_

    This class provides the non-linear optimization of the peak parameters
    
    Given a vector of peak shapes, this class optimizes all peak shapes parameters using a non-linear optimization
    For the non-linear optimization we use the Levenberg-Marquardt algorithm provided by the Eigen
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OptimizePick()
        """
        ...
    
    @overload
    def __init__(self, in_0: OptimizePick ) -> None:
        """
        Cython signature: void OptimizePick(OptimizePick &)
        """
        ...
    
    @overload
    def __init__(self, penalties_: OptimizationFunctions_PenaltyFactors , max_iteration_: int ) -> None:
        """
        Cython signature: void OptimizePick(OptimizationFunctions_PenaltyFactors penalties_, int max_iteration_)
        """
        ...
    
    def getPenalties(self) -> OptimizationFunctions_PenaltyFactors:
        """
        Cython signature: OptimizationFunctions_PenaltyFactors getPenalties()
        Returns the penalty factors
        """
        ...
    
    def setPenalties(self, penalties: OptimizationFunctions_PenaltyFactors ) -> None:
        """
        Cython signature: void setPenalties(OptimizationFunctions_PenaltyFactors penalties)
        Sets the penalty factors
        """
        ...
    
    def getNumberIterations(self) -> int:
        """
        Cython signature: unsigned int getNumberIterations()
        Returns the number of iterations
        """
        ...
    
    def setNumberIterations(self, max_iteration: int ) -> None:
        """
        Cython signature: void setNumberIterations(int max_iteration)
        Sets the number of iterations
        """
        ... 


class OptimizePick_Data:
    """
    Cython implementation of _OptimizePick_Data

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OptimizePick_Data.html>`_
    """
    
    positions: List[float]
    
    signal: List[float] 


class PSProteinInference:
    """
    Cython implementation of _PSProteinInference

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PSProteinInference.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PSProteinInference()
        """
        ...
    
    @overload
    def __init__(self, in_0: PSProteinInference ) -> None:
        """
        Cython signature: void PSProteinInference(PSProteinInference &)
        """
        ...
    
    def findMinimalProteinList(self, peptide_ids: List[PeptideIdentification] ) -> int:
        """
        Cython signature: size_t findMinimalProteinList(libcpp_vector[PeptideIdentification] & peptide_ids)
        """
        ...
    
    def calculateProteinProbabilities(self, ids: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void calculateProteinProbabilities(libcpp_vector[PeptideIdentification] & ids)
        """
        ...
    
    def getProteinProbability(self, acc: Union[bytes, str, String] ) -> float:
        """
        Cython signature: double getProteinProbability(const String & acc)
        """
        ...
    
    def isProteinInMinimalList(self, acc: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool isProteinInMinimalList(const String & acc)
        """
        ...
    
    def getNumberOfProtIds(self, protein_id_threshold: float ) -> int:
        """
        Cython signature: int getNumberOfProtIds(double protein_id_threshold)
        """
        ...
    
    def getSolver(self) -> int:
        """
        Cython signature: SOLVER getSolver()
        """
        ... 


class PScore:
    """
    Cython implementation of _PScore

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PScore.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PScore()
        """
        ...
    
    @overload
    def __init__(self, in_0: PScore ) -> None:
        """
        Cython signature: void PScore(PScore &)
        """
        ...
    
    def calculateIntensityRankInMZWindow(self, mz: List[float] , intensities: List[float] , mz_window: float ) -> List[int]:
        """
        Cython signature: libcpp_vector[size_t] calculateIntensityRankInMZWindow(libcpp_vector[double] & mz, libcpp_vector[double] & intensities, double mz_window)
        Calculate local (windowed) peak ranks
        
        The peak rank is defined as the number of neighboring peaks in +/- (mz_window/2) that have higher intensity
        The result can be used to efficiently filter spectra for top 1..n peaks in mass windows
        
        
        :param mz: The m/z positions of the peaks
        :param intensities: The intensities of the peaks
        :param mz_window: The window in Thomson centered at each peak
        """
        ...
    
    def calculateRankMap(self, peak_map: MSExperiment , mz_window: float ) -> List[List[int]]:
        """
        Cython signature: libcpp_vector[libcpp_vector[size_t]] calculateRankMap(MSExperiment & peak_map, double mz_window)
        Precalculated, windowed peak ranks for a whole experiment
        
        The peak rank is defined as the number of neighboring peaks in +/- (mz_window/2) that have higher intensity
        
        
        :param peak_map: Fragment spectra used for rank calculation. Typically a peak map after removal of all MS1 spectra
        :param mz_window: Window in Thomson centered at each peak
        """
        ...
    
    def calculatePeakLevelSpectra(self, spec: MSSpectrum , ranks: List[int] , min_level: int , max_level: int ) -> Dict[int, MSSpectrum]:
        """
        Cython signature: libcpp_map[size_t,MSSpectrum] calculatePeakLevelSpectra(MSSpectrum & spec, libcpp_vector[size_t] & ranks, size_t min_level, size_t max_level)
        Calculates spectra for peak level between min_level to max_level and stores them in the map
        
        A spectrum of peak level n retains the (n+1) top intensity peaks in a sliding mz_window centered at each peak
        """
        ...
    
    @overload
    def computePScore(self, fragment_mass_tolerance: float , fragment_mass_tolerance_unit_ppm: bool , peak_level_spectra: Dict[int, MSSpectrum] , theo_spectra: List[MSSpectrum] , mz_window: float ) -> float:
        """
        Cython signature: double computePScore(double fragment_mass_tolerance, bool fragment_mass_tolerance_unit_ppm, libcpp_map[size_t,MSSpectrum] & peak_level_spectra, libcpp_vector[MSSpectrum] & theo_spectra, double mz_window)
        Computes the PScore for a vector of theoretical spectra
        
        Similar to Andromeda, a vector of theoretical spectra can be provided that e.g. contain loss spectra or higher charge spectra depending on the sequence.
        The best score obtained by scoring all those theoretical spectra against the experimental ones is returned
        
        
        :param fragment_mass_tolerance: Mass tolerance for matching peaks
        :param fragment_mass_tolerance_unit_ppm: Whether Thomson or ppm is used
        :param peak_level_spectra: Spectra for different peak levels (=filtered by maximum rank).
        :param theo_spectra: Theoretical spectra as obtained e.g. from TheoreticalSpectrumGenerator
        :param mz_window: Window in Thomson centered at each peak
        """
        ...
    
    @overload
    def computePScore(self, fragment_mass_tolerance: float , fragment_mass_tolerance_unit_ppm: bool , peak_level_spectra: Dict[int, MSSpectrum] , theo_spectrum: MSSpectrum , mz_window: float ) -> float:
        """
        Cython signature: double computePScore(double fragment_mass_tolerance, bool fragment_mass_tolerance_unit_ppm, libcpp_map[size_t,MSSpectrum] & peak_level_spectra, MSSpectrum & theo_spectrum, double mz_window)
        Computes the PScore for a single theoretical spectrum
        
        
        :param fragment_mass_tolerance: Mass tolerance for matching peaks
        :param fragment_mass_tolerance_unit_ppm: Whether Thomson or ppm is used
        :param peak_level_spectra: Spectra for different peak levels (=filtered by maximum rank)
        :param theo_spectra: Theoretical spectra as obtained e.g. from TheoreticalSpectrumGenerator
        :param mz_window: Window in Thomson centered at each peak
        """
        ... 


class ParentPeakMower:
    """
    Cython implementation of _ParentPeakMower

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ParentPeakMower.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ParentPeakMower()
        """
        ...
    
    @overload
    def __init__(self, in_0: ParentPeakMower ) -> None:
        """
        Cython signature: void ParentPeakMower(ParentPeakMower &)
        """
        ...
    
    def filterSpectrum(self, spec: MSSpectrum ) -> None:
        """
        Cython signature: void filterSpectrum(MSSpectrum & spec)
        """
        ...
    
    def filterPeakSpectrum(self, spec: MSSpectrum ) -> None:
        """
        Cython signature: void filterPeakSpectrum(MSSpectrum & spec)
        """
        ...
    
    def filterPeakMap(self, exp: MSExperiment ) -> None:
        """
        Cython signature: void filterPeakMap(MSExperiment & exp)
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class PeptideEvidence:
    """
    Cython implementation of _PeptideEvidence

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PeptideEvidence.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PeptideEvidence()
        """
        ...
    
    @overload
    def __init__(self, in_0: PeptideEvidence ) -> None:
        """
        Cython signature: void PeptideEvidence(PeptideEvidence &)
        """
        ...
    
    def setStart(self, start: int ) -> None:
        """
        Cython signature: void setStart(int start)
        Sets the position of the last AA of the peptide in protein coordinates (starting at 0 for the N-terminus). If not available, set to UNKNOWN_POSITION. N-terminal positions must be marked with `N_TERMINAL_AA`
        """
        ...
    
    def getStart(self) -> int:
        """
        Cython signature: int getStart()
        Returns the position in the protein (starting at 0 for the N-terminus). If not available UNKNOWN_POSITION constant is returned
        """
        ...
    
    def setEnd(self, end: int ) -> None:
        """
        Cython signature: void setEnd(int end)
        Sets the position of the last AA of the peptide in protein coordinates (starting at 0 for the N-terminus). If not available, set UNKNOWN_POSITION. C-terminal positions must be marked with C_TERMINAL_AA
        """
        ...
    
    def getEnd(self) -> int:
        """
        Cython signature: int getEnd()
        Returns the position of the last AA of the peptide in protein coordinates (starting at 0 for the N-terminus). If not available UNKNOWN_POSITION constant is returned
        """
        ...
    
    def setAABefore(self, rhs: bytes ) -> None:
        """
        Cython signature: void setAABefore(char rhs)
        Sets the amino acid single letter code before the sequence (preceding amino acid in the protein). If not available, set to UNKNOWN_AA. If N-terminal set to N_TERMINAL_AA
        """
        ...
    
    def getAABefore(self) -> bytes:
        """
        Cython signature: char getAABefore()
        Returns the amino acid single letter code before the sequence (preceding amino acid in the protein). If not available, UNKNOWN_AA is returned. If N-terminal, N_TERMINAL_AA is returned
        """
        ...
    
    def setAAAfter(self, rhs: bytes ) -> None:
        """
        Cython signature: void setAAAfter(char rhs)
        Sets the amino acid single letter code after the sequence (subsequent amino acid in the protein). If not available, set to UNKNOWN_AA. If C-terminal set to C_TERMINAL_AA
        """
        ...
    
    def getAAAfter(self) -> bytes:
        """
        Cython signature: char getAAAfter()
        Returns the amino acid single letter code after the sequence (subsequent amino acid in the protein). If not available, UNKNOWN_AA is returned. If C-terminal, C_TERMINAL_AA is returned
        """
        ...
    
    def setProteinAccession(self, s: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setProteinAccession(String s)
        Sets the protein accession the peptide matches to. If not available set to empty string
        """
        ...
    
    def getProteinAccession(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getProteinAccession()
        Returns the protein accession the peptide matches to. If not available the empty string is returned
        """
        ...
    
    def hasValidLimits(self) -> bool:
        """
        Cython signature: bool hasValidLimits()
        Start and end numbers in evidence represent actual numeric indices
        """
        ...
    
    def __richcmp__(self, other: PeptideEvidence, op: int) -> Any:
        ... 


class PercolatorOutfile:
    """
    Cython implementation of _PercolatorOutfile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PercolatorOutfile.html>`_

    Class for reading Percolator tab-delimited output files
    
    For PSM-level output, the file extension should be ".psms"
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PercolatorOutfile()
        """
        ...
    
    @overload
    def __init__(self, in_0: PercolatorOutfile ) -> None:
        """
        Cython signature: void PercolatorOutfile(PercolatorOutfile &)
        """
        ...
    
    def getScoreType(self, score_type_name: Union[bytes, str, String] ) -> int:
        """
        Cython signature: PercolatorOutfile_ScoreType getScoreType(String score_type_name)
        Returns a score type given its name
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , proteins: ProteinIdentification , peptides: List[PeptideIdentification] , lookup: SpectrumMetaDataLookup , output_score: int ) -> None:
        """
        Cython signature: void load(const String & filename, ProteinIdentification & proteins, libcpp_vector[PeptideIdentification] & peptides, SpectrumMetaDataLookup & lookup, PercolatorOutfile_ScoreType output_score)
        Loads a Percolator output file
        """
        ...
    PercolatorOutfile_ScoreType : __PercolatorOutfile_ScoreType 


class PrecursorIonSelectionPreprocessing:
    """
    Cython implementation of _PrecursorIonSelectionPreprocessing

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PrecursorIonSelectionPreprocessing.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PrecursorIonSelectionPreprocessing()
        """
        ...
    
    @overload
    def __init__(self, in_0: PrecursorIonSelectionPreprocessing ) -> None:
        """
        Cython signature: void PrecursorIonSelectionPreprocessing(PrecursorIonSelectionPreprocessing &)
        """
        ...
    
    def getMasses(self, acc: Union[bytes, str, String] ) -> List[float]:
        """
        Cython signature: libcpp_vector[double] getMasses(String acc)
        """
        ...
    
    @overload
    def dbPreprocessing(self, db_path: Union[bytes, str, String] , save: bool ) -> None:
        """
        Cython signature: void dbPreprocessing(String db_path, bool save)
        Calculates tryptic peptide masses of a given database and stores masses and peptide sequences
        
        
        :param db_path: Path to database file (fasta)
        :param save: Flag if preprocessing should be stored
        :raises:
          Exception: FileNotFound is thrown if the file could not be found
        :raises:
          Exception: UnableToCreateFile if preprocessing file can't be written
        """
        ...
    
    @overload
    def dbPreprocessing(self, db_path: Union[bytes, str, String] , rt_model_path: Union[bytes, str, String] , dt_model_path: Union[bytes, str, String] , save: bool ) -> None:
        """
        Cython signature: void dbPreprocessing(String db_path, String rt_model_path, String dt_model_path, bool save)
        Calculates tryptic peptide masses of a given database and stores masses and peptide sequences
        
        
        :param db_path: Path to database file (fasta)
        :param rt_model_path: Path to the retention time model
        :param dt_model_path: Path to the detectability model
        :param save: Flag if preprocessing should be stored
        :raises:
          Exception: FileNotFound is thrown if the file could not be found
        :raises:
          Exception: UnableToCreateFile if preprocessing file can't be written
        """
        ...
    
    def loadPreprocessing(self) -> None:
        """
        Cython signature: void loadPreprocessing()
        Loads tryptic peptide masses of a given database
        """
        ...
    
    def getWeight(self, mass: float ) -> float:
        """
        Cython signature: double getWeight(double mass)
        Returns the weighted frequency of a mass
        """
        ...
    
    def getRT(self, prot_id: Union[bytes, str, String] , peptide_index: int ) -> float:
        """
        Cython signature: double getRT(String prot_id, size_t peptide_index)
        Returns the RT value
        """
        ...
    
    def getPT(self, prot_id: Union[bytes, str, String] , peptide_index: int ) -> float:
        """
        Cython signature: double getPT(String prot_id, size_t peptide_index)
        Returns the PT value
        """
        ...
    
    def setFixedModifications(self, modifications: List[bytes] ) -> None:
        """
        Cython signature: void setFixedModifications(StringList & modifications)
        """
        ...
    
    def setGaussianParameters(self, mu: float , sigma: float ) -> None:
        """
        Cython signature: void setGaussianParameters(double mu, double sigma)
        """
        ...
    
    def getGaussMu(self) -> float:
        """
        Cython signature: double getGaussMu()
        Returns the Gauss Mu value
        """
        ...
    
    def getGaussSigma(self) -> float:
        """
        Cython signature: double getGaussSigma()
        Returns the Gauss Sigma value
        """
        ...
    
    @overload
    def getRTProbability(self, prot_id: Union[bytes, str, String] , peptide_index: int , feature: Feature ) -> float:
        """
        Cython signature: double getRTProbability(String prot_id, size_t peptide_index, Feature & feature)
        """
        ...
    
    @overload
    def getRTProbability(self, pred_rt: float , feature: Feature ) -> float:
        """
        Cython signature: double getRTProbability(double pred_rt, Feature & feature)
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class ProteinInference:
    """
    Cython implementation of _ProteinInference

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ProteinInference.html>`_

    [experimental class] given a peptide quantitation, infer corresponding protein quantities
    
    Infers protein ratios from peptide ratios (currently using unique peptides only).
    Use the IDMapper class to add protein and peptide information to a
    quantitative ConsensusMap prior to this step
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ProteinInference()
        """
        ...
    
    @overload
    def __init__(self, in_0: ProteinInference ) -> None:
        """
        Cython signature: void ProteinInference(ProteinInference &)
        """
        ...
    
    def infer(self, consensus_map: ConsensusMap , reference_map: int ) -> None:
        """
        Cython signature: void infer(ConsensusMap & consensus_map, unsigned int reference_map)
        Given a peptide quantitation, infer corresponding protein quantities
        
        Infers protein ratios from peptide ratios (currently using unique peptides only).
        Use the IDMapper class to add protein and peptide information to a
        quantitative ConsensusMap prior to this step
        
        
        :param consensus_map: Peptide quantitation with ProteinIdentifications attached, where protein quantitation will be attached
        :param reference_map: Index of (iTRAQ) reference channel within the consensus map
        """
        ... 


class QTCluster:
    """
    Cython implementation of _QTCluster

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1QTCluster.html>`_
    """
    
    def __init__(self, in_0: QTCluster ) -> None:
        """
        Cython signature: void QTCluster(QTCluster &)
        """
        ...
    
    def getCenterRT(self) -> float:
        """
        Cython signature: double getCenterRT()
        Returns the RT value of the cluster
        """
        ...
    
    def getCenterMZ(self) -> float:
        """
        Cython signature: double getCenterMZ()
        Returns the m/z value of the cluster center
        """
        ...
    
    def getXCoord(self) -> int:
        """
        Cython signature: int getXCoord()
        Returns the x coordinate in the grid
        """
        ...
    
    def getYCoord(self) -> int:
        """
        Cython signature: int getYCoord()
        Returns the y coordinate in the grid
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: size_t size()
        Returns the size of the cluster (number of elements, incl. center)
        """
        ...
    
    def getQuality(self) -> float:
        """
        Cython signature: double getQuality()
        Returns the cluster quality and recomputes if necessary
        """
        ...
    
    def getAnnotations(self) -> Set[AASequence]:
        """
        Cython signature: libcpp_set[AASequence] getAnnotations()
        Returns the set of peptide sequences annotated to the cluster center
        """
        ...
    
    def setInvalid(self) -> None:
        """
        Cython signature: void setInvalid()
        Sets current cluster as invalid (also frees some memory)
        """
        ...
    
    def isInvalid(self) -> bool:
        """
        Cython signature: bool isInvalid()
        Whether current cluster is invalid
        """
        ...
    
    def initializeCluster(self) -> None:
        """
        Cython signature: void initializeCluster()
        Has to be called before adding elements (calling
        """
        ...
    
    def finalizeCluster(self) -> None:
        """
        Cython signature: void finalizeCluster()
        Has to be called after adding elements (after calling
        """
        ...
    
    def __richcmp__(self, other: QTCluster, op: int) -> Any:
        ... 


class QTClusterFinder:
    """
    Cython implementation of _QTClusterFinder

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1QTClusterFinder.html>`_
      -- Inherits from ['BaseGroupFinder']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void QTClusterFinder()
        """
        ...
    
    @overload
    def run(self, input_maps: List[ConsensusMap] , result_map: ConsensusMap ) -> None:
        """
        Cython signature: void run(libcpp_vector[ConsensusMap] & input_maps, ConsensusMap & result_map)
        """
        ...
    
    @overload
    def run(self, input_maps: List[FeatureMap] , result_map: ConsensusMap ) -> None:
        """
        Cython signature: void run(libcpp_vector[FeatureMap] & input_maps, ConsensusMap & result_map)
        """
        ...
    
    def getProductName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getProductName()
        Returns the name of the product
        """
        ...
    
    def registerChildren(self) -> None:
        """
        Cython signature: void registerChildren()
        Register all derived classes here
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ...
    
    def setLogType(self, in_0: int ) -> None:
        """
        Cython signature: void setLogType(LogType)
        Sets the progress log that should be used. The default type is NONE!
        """
        ...
    
    def getLogType(self) -> int:
        """
        Cython signature: LogType getLogType()
        Returns the type of progress log being used
        """
        ...
    
    def startProgress(self, begin: int , end: int , label: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void startProgress(ptrdiff_t begin, ptrdiff_t end, String label)
        """
        ...
    
    def setProgress(self, value: int ) -> None:
        """
        Cython signature: void setProgress(ptrdiff_t value)
        Sets the current progress
        """
        ...
    
    def endProgress(self) -> None:
        """
        Cython signature: void endProgress()
        Ends the progress display
        """
        ...
    
    def nextProgress(self) -> None:
        """
        Cython signature: void nextProgress()
        Increment progress by 1 (according to range begin-end)
        """
        ... 


class RansacModelLinear:
    """
    Cython implementation of _RansacModelLinear

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Math_1_1RansacModelLinear.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void RansacModelLinear()
        """
        ...
    
    @overload
    def __init__(self, in_0: RansacModelLinear ) -> None:
        """
        Cython signature: void RansacModelLinear(RansacModelLinear &)
        """
        ... 


class RipFileContent:
    """
    Cython implementation of _RipFileContent

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::IDRipper_1_1RipFileContent.html>`_
    """
    
    def __init__(self, prot_idents: List[ProteinIdentification] , pep_idents: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void RipFileContent(libcpp_vector[ProteinIdentification] & prot_idents, libcpp_vector[PeptideIdentification] & pep_idents)
        """
        ...
    
    def getProteinIdentifications(self) -> List[ProteinIdentification]:
        """
        Cython signature: libcpp_vector[ProteinIdentification] getProteinIdentifications()
        """
        ...
    
    def getPeptideIdentifications(self) -> List[PeptideIdentification]:
        """
        Cython signature: libcpp_vector[PeptideIdentification] getPeptideIdentifications()
        """
        ... 


class RipFileIdentifier:
    """
    Cython implementation of _RipFileIdentifier

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::IDRipper_1_1RipFileIdentifier.html>`_
    """
    
    def __init__(self, id_runs: IdentificationRuns , pep_id: PeptideIdentification , file_origin_map: Dict[Union[bytes, str, String], int] , origin_annotation_fmt: int , split_ident_runs: bool ) -> None:
        """
        Cython signature: void RipFileIdentifier(IdentificationRuns & id_runs, PeptideIdentification & pep_id, libcpp_map[String,unsigned int] & file_origin_map, OriginAnnotationFormat origin_annotation_fmt, bool split_ident_runs)
        """
        ...
    
    def getIdentRunIdx(self) -> int:
        """
        Cython signature: unsigned int getIdentRunIdx()
        """
        ...
    
    def getFileOriginIdx(self) -> int:
        """
        Cython signature: unsigned int getFileOriginIdx()
        """
        ...
    
    def getOriginFullname(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getOriginFullname()
        """
        ...
    
    def getOutputBasename(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getOutputBasename()
        """
        ... 


class Sample:
    """
    Cython implementation of _Sample

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Sample.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Sample()
        """
        ...
    
    @overload
    def __init__(self, in_0: Sample ) -> None:
        """
        Cython signature: void Sample(Sample &)
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(String name)
        """
        ...
    
    def getOrganism(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getOrganism()
        """
        ...
    
    def setOrganism(self, organism: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setOrganism(String organism)
        """
        ...
    
    def getNumber(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getNumber()
        Returns the sample number
        """
        ...
    
    def setNumber(self, number: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setNumber(String number)
        Sets the sample number (e.g. sample ID)
        """
        ...
    
    def getComment(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getComment()
        Returns the comment (default "")
        """
        ...
    
    def setComment(self, comment: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setComment(String comment)
        Sets the comment (may contain newline characters)
        """
        ...
    
    def getState(self) -> int:
        """
        Cython signature: SampleState getState()
        Returns the state of aggregation (default SAMPLENULL)
        """
        ...
    
    def setState(self, state: int ) -> None:
        """
        Cython signature: void setState(SampleState state)
        Sets the state of aggregation
        """
        ...
    
    def getMass(self) -> float:
        """
        Cython signature: double getMass()
        Returns the mass (in gram) (default 0.0)
        """
        ...
    
    def setMass(self, mass: float ) -> None:
        """
        Cython signature: void setMass(double mass)
        Sets the mass (in gram)
        """
        ...
    
    def getVolume(self) -> float:
        """
        Cython signature: double getVolume()
        Returns the volume (in ml) (default 0.0)
        """
        ...
    
    def setVolume(self, volume: float ) -> None:
        """
        Cython signature: void setVolume(double volume)
        Sets the volume (in ml)
        """
        ...
    
    def getConcentration(self) -> float:
        """
        Cython signature: double getConcentration()
        Returns the concentration (in g/l) (default 0.0)
        """
        ...
    
    def setConcentration(self, concentration: float ) -> None:
        """
        Cython signature: void setConcentration(double concentration)
        Sets the concentration (in g/l)
        """
        ...
    
    def getSubsamples(self) -> List[Sample]:
        """
        Cython signature: libcpp_vector[Sample] getSubsamples()
        Returns a reference to the vector of subsamples that were combined to create this sample
        """
        ...
    
    def setSubsamples(self, subsamples: List[Sample] ) -> None:
        """
        Cython signature: void setSubsamples(libcpp_vector[Sample] subsamples)
        Sets the vector of subsamples that were combined to create this sample
        """
        ...
    
    def removeTreatment(self, position: int ) -> None:
        """
        Cython signature: void removeTreatment(unsigned int position)
        Brief removes the sample treatment at the given position
        """
        ...
    
    def countTreatments(self) -> int:
        """
        Cython signature: int countTreatments()
        Returns the number of sample treatments
        """
        ...
    
    def isMetaEmpty(self) -> bool:
        """
        Cython signature: bool isMetaEmpty()
        Returns if the MetaInfo is empty
        """
        ...
    
    def clearMetaInfo(self) -> None:
        """
        Cython signature: void clearMetaInfo()
        Removes all meta values
        """
        ...
    
    def metaRegistry(self) -> MetaInfoRegistry:
        """
        Cython signature: MetaInfoRegistry metaRegistry()
        Returns a reference to the MetaInfoRegistry
        """
        ...
    
    def getKeys(self, keys: List[bytes] ) -> None:
        """
        Cython signature: void getKeys(libcpp_vector[String] & keys)
        Fills the given vector with a list of all keys for which a value is set
        """
        ...
    
    def getMetaValue(self, in_0: Union[bytes, str, String] ) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getMetaValue(String)
        Returns the value corresponding to a string, or
        """
        ...
    
    def setMetaValue(self, in_0: Union[bytes, str, String] , in_1: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setMetaValue(String, DataValue)
        Sets the DataValue corresponding to a name
        """
        ...
    
    def metaValueExists(self, in_0: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool metaValueExists(String)
        Returns whether an entry with the given name exists
        """
        ...
    
    def removeMetaValue(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void removeMetaValue(String)
        Removes the DataValue corresponding to `name` if it exists
        """
        ...
    
    def __richcmp__(self, other: Sample, op: int) -> Any:
        ...
    SampleState : __SampleState 


class SiriusAdapterHit:
    """
    Cython implementation of _SiriusAdapterHit

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::SiriusMzTabWriter_1_1SiriusAdapterHit.html>`_
    """
    
    formula: Union[bytes, str, String]
    
    adduct: Union[bytes, str, String]
    
    precursor_formula: Union[bytes, str, String]
    
    rank: int
    
    iso_score: float
    
    tree_score: float
    
    sirius_score: float
    
    explainedpeaks: int
    
    explainedintensity: float
    
    median_mass_error_fragment_peaks_ppm: float
    
    median_absolute_mass_error_fragment_peaks_ppm: float
    
    mass_error_precursor_ppm: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SiriusAdapterHit()
        """
        ...
    
    @overload
    def __init__(self, in_0: SiriusAdapterHit ) -> None:
        """
        Cython signature: void SiriusAdapterHit(SiriusAdapterHit &)
        """
        ... 


class SourceFile:
    """
    Cython implementation of _SourceFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SourceFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SourceFile()
        Description of a file location, used to store the origin of (meta) data
        """
        ...
    
    @overload
    def __init__(self, in_0: SourceFile ) -> None:
        """
        Cython signature: void SourceFile(SourceFile &)
        """
        ...
    
    def getNameOfFile(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getNameOfFile()
        Returns the file name
        """
        ...
    
    def setNameOfFile(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setNameOfFile(String)
        Sets the file name
        """
        ...
    
    def getPathToFile(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getPathToFile()
        Returns the file path
        """
        ...
    
    def setPathToFile(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setPathToFile(String)
        Sets the file path
        """
        ...
    
    def getFileSize(self) -> float:
        """
        Cython signature: float getFileSize()
        Returns the file size in MB
        """
        ...
    
    def setFileSize(self, in_0: float ) -> None:
        """
        Cython signature: void setFileSize(float)
        Sets the file size in MB
        """
        ...
    
    def getFileType(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getFileType()
        Returns the file type
        """
        ...
    
    def setFileType(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setFileType(String)
        Sets the file type
        """
        ...
    
    def getChecksum(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getChecksum()
        Returns the file's checksum
        """
        ...
    
    def setChecksum(self, in_0: Union[bytes, str, String] , in_1: int ) -> None:
        """
        Cython signature: void setChecksum(String, ChecksumType)
        Sets the file's checksum
        """
        ...
    
    def getChecksumType(self) -> int:
        """
        Cython signature: ChecksumType getChecksumType()
        Returns the checksum type
        """
        ...
    
    def getNativeIDType(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getNativeIDType()
        Returns the native ID type of the spectra
        """
        ...
    
    def setNativeIDType(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setNativeIDType(String)
        Sets the native ID type of the spectra
        """
        ...
    
    def getNativeIDTypeAccession(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getNativeIDTypeAccession()
        Returns the nativeID of the spectra
        """
        ...
    
    def setNativeIDTypeAccession(self, accesssion: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setNativeIDTypeAccession(const String & accesssion)
        Sets the native ID of the spectra
        """
        ... 


class TheoreticalSpectrumGenerator:
    """
    Cython implementation of _TheoreticalSpectrumGenerator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TheoreticalSpectrumGenerator.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TheoreticalSpectrumGenerator()
        """
        ...
    
    @overload
    def __init__(self, in_0: TheoreticalSpectrumGenerator ) -> None:
        """
        Cython signature: void TheoreticalSpectrumGenerator(TheoreticalSpectrumGenerator &)
        """
        ...
    
    def getSpectrum(self, spec: MSSpectrum , peptide: AASequence , min_charge: int , max_charge: int ) -> None:
        """
        Cython signature: void getSpectrum(MSSpectrum & spec, AASequence & peptide, int min_charge, int max_charge)
        Generates a spectrum for a peptide sequence, with the ion types that are set in the tool parameters. If precursor_charge is set to 0 max_charge + 1 will be used
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class TransformationXMLFile:
    """
    Cython implementation of _TransformationXMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TransformationXMLFile.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void TransformationXMLFile()
        """
        ...
    
    def load(self, in_0: Union[bytes, str, String] , in_1: TransformationDescription , fit_model: bool ) -> None:
        """
        Cython signature: void load(String, TransformationDescription &, bool fit_model)
        """
        ...
    
    def store(self, in_0: Union[bytes, str, String] , in_1: TransformationDescription ) -> None:
        """
        Cython signature: void store(String, TransformationDescription)
        """
        ... 


class streampos:
    """
    Cython implementation of _streampos

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classstd_1_1streampos.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void streampos()
        """
        ...
    
    @overload
    def __init__(self, in_0: streampos ) -> None:
        """
        Cython signature: void streampos(streampos &)
        """
        ... 


class __ByteOrder:
    None
    BYTEORDER_BIGENDIAN : int
    BYTEORDER_LITTLEENDIAN : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class ChecksumType:
    None
    UNKNOWN_CHECKSUM : int
    SHA1 : int
    MD5 : int
    SIZE_OF_CHECKSUMTYPE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class DataType:
    None
    STRING_VALUE : int
    INT_VALUE : int
    DOUBLE_VALUE : int
    STRING_LIST : int
    INT_LIST : int
    DOUBLE_LIST : int
    EMPTY_VALUE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class FileType:
    None
    UNKNOWN : int
    DTA : int
    DTA2D : int
    MZDATA : int
    MZXML : int
    FEATUREXML : int
    IDXML : int
    CONSENSUSXML : int
    MGF : int
    INI : int
    TOPPAS : int
    TRANSFORMATIONXML : int
    MZML : int
    CACHEDMZML : int
    MS2 : int
    PEPXML : int
    PROTXML : int
    MZIDENTML : int
    MZQUANTML : int
    QCML : int
    GELML : int
    TRAML : int
    MSP : int
    OMSSAXML : int
    MASCOTXML : int
    PNG : int
    XMASS : int
    TSV : int
    PEPLIST : int
    HARDKLOER : int
    KROENIK : int
    FASTA : int
    EDTA : int
    CSV : int
    TXT : int
    OBO : int
    HTML : int
    XML : int
    ANALYSISXML : int
    XSD : int
    PSQ : int
    MRM : int
    SQMASS : int
    PQP : int
    OSW : int
    PSMS : int
    PARAMXML : int
    SIZE_OF_TYPE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class ITRAQ_TYPES:
    None
    FOURPLEX : int
    EIGHTPLEX : int
    TMT_SIXPLEX : int
    SIZE_OF_ITRAQ_TYPES : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class OriginAnnotationFormat:
    None
    FILE_ORIGIN : int
    MAP_INDEX : int
    ID_MERGE_INDEX : int
    UNKNOWN_OAF : int
    SIZE_OF_ORIGIN_ANNOTATION_FORMAT : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __PercolatorOutfile_ScoreType:
    None
    QVALUE : int
    POSTERRPROB : int
    SCORE : int
    SIZE_OF_SCORETYPE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class SIDE:
    None
    LEFT : int
    RIGHT : int
    BOTH : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __SampleState:
    None
    SAMPLENULL : int
    SOLID : int
    LIQUID : int
    GAS : int
    SOLUTION : int
    EMULSION : int
    SUSPENSION : int
    SIZE_OF_SAMPLESTATE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class ScanMode:
    None
    UNKNOWN : int
    MASSSPECTRUM : int
    MS1SPECTRUM : int
    MSNSPECTRUM : int
    SIM : int
    SRM : int
    CRM : int
    CNG : int
    CNL : int
    PRECURSOR : int
    EMC : int
    TDF : int
    EMR : int
    EMISSION : int
    ABSORPTION : int
    SIZE_OF_SCANMODE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __Specificity:
    None
    SPEC_NONE : int
    SPEC_SEMI : int
    SPEC_FULL : int
    SPEC_UNKNOWN : int
    SPEC_NOCTERM : int
    SPEC_NONTERM : int
    SIZE_OF_SPECIFICITY : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class UnitType:
    None
    UNIT_ONTOLOGY : int
    MS_ONTOLOGY : int
    OTHER : int

    def getMapping(self) -> Dict[int, str]:
       ... 

