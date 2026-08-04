package mt5grpc

import (
	"github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/core/enums"
	core "github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/core/types"
	"github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/internal/pb"
	"github.com/jinzhu/copier"
)

func NewFromProto(p *pb.Error) *core.Error {
	if p == nil {
		return nil
	}
	return &core.Error{Code: enums.ErrorCode(p.GetCode()), Message: p.GetMessage()}
}

type Response interface {
	GetError() *pb.Error
}

func ValidateMT5GRPCResponse(resp Response) error {
	if errProto := resp.GetError(); errProto.GetCode() != int32(enums.ErrorCode_RES_S_OK) { // Domain error
		return NewFromProto(errProto)
	}
	return nil
}

func ParseMT5GRPCResponse[TSource any, TDest any](resp Response, getResult func() TSource) (*TDest, error) {
	//if errProto := resp.GetError(); errProto.GetCode() != int32(core.ErrorCode_RES_S_OK) { // Domain error
	//	return nil, NewFromProto(errProto)
	//}
	err := ValidateMT5GRPCResponse(resp)
	if err != nil {
		return nil, err
	}

	dst := new(TDest)
	err = copier.Copy(dst, getResult())
	if err != nil {
		return nil, err
	}

	return dst, nil
}
func DereferenceListResponse[TDest any](list *[]TDest, err error) ([]TDest, error) {
	if list == nil {
		return nil, err
	}
	return *list, nil

}

//func DereferenceList[TDest any](f func() (*[]TDest, error)) ([]TDest, error) {
//	r, err := f()
//	if r == nil {
//		return nil, err
//	}
//	return *r, err
//}
