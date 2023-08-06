/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* TypeDef Definitions                                                        *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#ifdef GET_TYPEDEF_LIST
#undef GET_TYPEDEF_LIST

::mlir::nvgpu::DeviceAsyncTokenType,
::mlir::nvgpu::MBarrierType,
::mlir::nvgpu::MBarrierTokenType

#endif  // GET_TYPEDEF_LIST

#ifdef GET_TYPEDEF_CLASSES
#undef GET_TYPEDEF_CLASSES

static ::mlir::OptionalParseResult generatedTypeParser(::mlir::AsmParser &parser, ::llvm::StringRef *mnemonic, ::mlir::Type &value) {
  return ::mlir::AsmParser::KeywordSwitch<::mlir::OptionalParseResult>(parser)
    .Case(::mlir::nvgpu::DeviceAsyncTokenType::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::nvgpu::DeviceAsyncTokenType::get(parser.getContext());
      return ::mlir::success(!!value);
    })
    .Case(::mlir::nvgpu::MBarrierType::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::nvgpu::MBarrierType::parse(parser);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::nvgpu::MBarrierTokenType::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::nvgpu::MBarrierTokenType::get(parser.getContext());
      return ::mlir::success(!!value);
    })
    .Default([&](llvm::StringRef keyword, llvm::SMLoc) {
      *mnemonic = keyword;
      return std::nullopt;
    });
}

static ::mlir::LogicalResult generatedTypePrinter(::mlir::Type def, ::mlir::AsmPrinter &printer) {
  return ::llvm::TypeSwitch<::mlir::Type, ::mlir::LogicalResult>(def)    .Case<::mlir::nvgpu::DeviceAsyncTokenType>([&](auto t) {
      printer << ::mlir::nvgpu::DeviceAsyncTokenType::getMnemonic();
      return ::mlir::success();
    })
    .Case<::mlir::nvgpu::MBarrierType>([&](auto t) {
      printer << ::mlir::nvgpu::MBarrierType::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::nvgpu::MBarrierTokenType>([&](auto t) {
      printer << ::mlir::nvgpu::MBarrierTokenType::getMnemonic();
      return ::mlir::success();
    })
    .Default([](auto) { return ::mlir::failure(); });
}

namespace mlir {
namespace nvgpu {
} // namespace nvgpu
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::nvgpu::DeviceAsyncTokenType)
namespace mlir {
namespace nvgpu {
namespace detail {
struct MBarrierTypeStorage : public ::mlir::TypeStorage {
  using KeyTy = std::tuple<Attribute>;
  MBarrierTypeStorage(Attribute memorySpace) : memorySpace(memorySpace) {}

  KeyTy getAsKey() const {
    return KeyTy(memorySpace);
  }

  bool operator==(const KeyTy &tblgenKey) const {
    return (memorySpace == std::get<0>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey));
  }

  static MBarrierTypeStorage *construct(::mlir::TypeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto memorySpace = std::get<0>(tblgenKey);
    return new (allocator.allocate<MBarrierTypeStorage>()) MBarrierTypeStorage(memorySpace);
  }

  Attribute memorySpace;
};
} // namespace detail
MBarrierType MBarrierType::get(::mlir::MLIRContext *context, Attribute memorySpace) {
  return Base::get(context, memorySpace);
}

::mlir::Type MBarrierType::parse(::mlir::AsmParser &odsParser) {
  ::mlir::Builder odsBuilder(odsParser.getContext());
  ::llvm::SMLoc odsLoc = odsParser.getCurrentLocation();
  (void) odsLoc;
  ::mlir::FailureOr<Attribute> _result_memorySpace;
  // Parse literal '<'
  if (odsParser.parseLess()) return {};
  // Parse parameter struct
  bool _seen_memorySpace = false;
  {
    const auto _loop_body = [&](::llvm::StringRef _paramKey) -> bool {
      // Parse literal '='
      if (odsParser.parseEqual()) return {};
      if (!_seen_memorySpace && _paramKey == "memorySpace") {
        _seen_memorySpace = true;

        // Parse variable 'memorySpace'
        _result_memorySpace = ::mlir::FieldParser<Attribute>::parse(odsParser);
        if (::mlir::failed(_result_memorySpace)) {
          odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse NVGPU_MBarrier parameter 'memorySpace' which is to be a `Attribute`");
          return {};
        }
      } else {
        odsParser.emitError(odsParser.getCurrentLocation(), "duplicate or unknown struct parameter name: ") << _paramKey;
        return {};
      }
      return true;
    };
    for (unsigned odsStructIndex = 0; odsStructIndex < 1; ++odsStructIndex) {
      ::llvm::StringRef _paramKey;
      if (odsParser.parseKeyword(&_paramKey)) {
        odsParser.emitError(odsParser.getCurrentLocation(),
                           "expected a parameter name in struct");
        return {};
      }
      if (!_loop_body(_paramKey)) return {};
      if ((odsStructIndex != 1 - 1) && odsParser.parseComma())
        return {};
    }
  }
  // Parse literal '>'
  if (odsParser.parseGreater()) return {};
  assert(::mlir::succeeded(_result_memorySpace));
  return MBarrierType::get(odsParser.getContext(),
      Attribute((*_result_memorySpace)));
}

void MBarrierType::print(::mlir::AsmPrinter &odsPrinter) const {
  ::mlir::Builder odsBuilder(getContext());
  odsPrinter << "<";
  {
    bool _firstPrinted = true;
    if (!_firstPrinted) odsPrinter << ", ";
    _firstPrinted = false;
    odsPrinter << "memorySpace = ";
    odsPrinter.printStrippedAttrOrType(getMemorySpace());
  }
  odsPrinter << ">";
}

Attribute MBarrierType::getMemorySpace() const {
  return getImpl()->memorySpace;
}

} // namespace nvgpu
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::nvgpu::MBarrierType)
namespace mlir {
namespace nvgpu {
} // namespace nvgpu
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::nvgpu::MBarrierTokenType)
namespace mlir {
namespace nvgpu {

/// Parse a type registered to this dialect.
::mlir::Type NVGPUDialect::parseType(::mlir::DialectAsmParser &parser) const {
  ::llvm::SMLoc typeLoc = parser.getCurrentLocation();
  ::llvm::StringRef mnemonic;
  ::mlir::Type genType;
  auto parseResult = generatedTypeParser(parser, &mnemonic, genType);
  if (parseResult.has_value())
    return genType;
  
  parser.emitError(typeLoc) << "unknown  type `"
      << mnemonic << "` in dialect `" << getNamespace() << "`";
  return {};
}
/// Print a type registered to this dialect.
void NVGPUDialect::printType(::mlir::Type type,
                    ::mlir::DialectAsmPrinter &printer) const {
  if (::mlir::succeeded(generatedTypePrinter(type, printer)))
    return;
  
}
} // namespace nvgpu
} // namespace mlir

#endif  // GET_TYPEDEF_CLASSES

