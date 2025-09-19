package client

import (
	"github.com/hybrid-syntax/mt5-grpc/go/mt5grpc"
	"github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/core/types"
	pb "github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/generated_proto" // import generated proto
	"github.com/jinzhu/copier"
	"google.golang.org/protobuf/types/known/emptypb"
)

func (c *Client) AccountInfo() (*types.AccountInfo, error) {
	resp, err := c.api.AccountInfo(c.ctx, &emptypb.Empty{})
	if err != nil {
		return nil, err
	}

	return mt5grpc.ParseMT5GRPCResponse[*pb.AccountInfo, types.AccountInfo](resp,
		func() *pb.AccountInfo {
			return resp.GetAccountInfo()
		})
}

func (c *Client) TerminalInfo() (*types.TerminalInfo, error) {
	resp, err := c.api.TerminalInfo(c.ctx, &emptypb.Empty{})
	if err != nil {
		return nil, err
	}

	return mt5grpc.ParseMT5GRPCResponse[*pb.TerminalInfo, types.TerminalInfo](resp,
		func() *pb.TerminalInfo {
			return resp.GetTerminalInfo()
		})
}

func (c *Client) Version() (*types.Version, error) {
	resp, err := c.api.Version(c.ctx, &emptypb.Empty{})
	if err != nil {
		return nil, err
	}

	return mt5grpc.ParseMT5GRPCResponse[*pb.Version, types.Version](resp,
		func() *pb.Version {
			return resp.GetVersion()
		})
}

func (c *Client) LastError() (*types.Error, error) {

	resp, err := c.api.LastError(c.ctx, &emptypb.Empty{})
	if err != nil {
		return nil, err
	}

	mt5error := new(types.Error)
	err = copier.Copy(&mt5error, resp.GetError())

	return mt5error, nil
}

func (c *Client) Initialize(path string, server string, login int64, password string) (bool, error) {
	req := &pb.InitializeRequest{
		Path:     path,
		Server:   server,
		Login:    login,
		Password: password,
	}

	resp, err := c.api.Initialize(c.ctx, req)
	if err != nil {
		return false, err
	}
	err = mt5grpc.ValidateMT5GRPCResponse(resp)
	if err != nil {
		return false, err
	}

	return resp.GetSuccess(), nil
}

func (c *Client) Login(login int64, password string, server string) (bool, error) {
	req := &pb.LoginRequest{
		Login:    login,
		Password: password,
		Server:   server,
	}

	resp, err := c.api.Login(c.ctx, req)
	if err != nil {
		return false, err
	}
	err = mt5grpc.ValidateMT5GRPCResponse(resp)
	if err != nil {
		return false, err
	}

	return resp.GetSuccess(), nil
}

func (c *Client) Shutdown() (bool, error) {
	resp, err := c.api.Shutdown(c.ctx, &emptypb.Empty{})
	if err != nil {
		return false, err
	}

	err = mt5grpc.ValidateMT5GRPCResponse(resp)
	if err != nil {
		return false, err
	}

	return resp.Success, nil
}

type BuyOption func(request *pb.BuyRequest)

func BuyWithComment(comment string) BuyOption {
	return func(r *pb.BuyRequest) { r.Comment = &comment }
}
func BuyWithPrice(price float64) BuyOption {
	return func(r *pb.BuyRequest) { r.Price = &price }
}
func BuyWithTicket(ticket int64) BuyOption {
	return func(r *pb.BuyRequest) { r.Ticket = &ticket }
}

func (c *Client) Buy(
	symbol string,
	volume float64,
	opts ...BuyOption) (*types.OrderSendResult, error) {

	req := &pb.BuyRequest{
		Symbol: symbol,
		Volume: volume,
	}

	for _, opt := range opts {
		opt(req)
	}

	resp, err := c.api.Buy(c.ctx, req)

	if err != nil {
		return nil, err
	}

	return mt5grpc.ParseMT5GRPCResponse[*pb.OrderSendResult, types.OrderSendResult](resp, func() *pb.OrderSendResult {
		return resp.GetOrderSendResult()
	})
}

type SellOption func(request *pb.SellRequest)

func SellWithComment(comment string) SellOption {
	return func(r *pb.SellRequest) { r.Comment = &comment }
}
func SellWithPrice(price float64) SellOption {
	return func(r *pb.SellRequest) { r.Price = &price }
}
func SellWithTicket(ticket int64) SellOption {
	return func(r *pb.SellRequest) { r.Ticket = &ticket }
}

func (c *Client) Sell(
	symbol string,
	volume float64,
	opts ...SellOption) (*types.OrderSendResult, error) {
	req := &pb.SellRequest{
		Symbol: symbol,
		Volume: volume,
	}

	for _, opt := range opts {
		opt(req)
	}

	resp, err := c.api.Sell(c.ctx, req)

	if err != nil {
		return nil, err
	}

	return mt5grpc.ParseMT5GRPCResponse[*pb.OrderSendResult, types.OrderSendResult](resp, func() *pb.OrderSendResult {
		return resp.GetOrderSendResult()
	})
}

type CloseOption func(request *pb.CloseRequest)

func CloseWithComment(comment string) CloseOption {
	return func(r *pb.CloseRequest) { r.Comment = &comment }
}

func CloseWithTicket(ticket int64) CloseOption {
	return func(r *pb.CloseRequest) { r.Ticket = &ticket }
}

func (c *Client) Close(symbol string, opts ...CloseOption) (*types.OrderSendResult, error) {
	req := &pb.CloseRequest{
		Symbol: symbol,
	}

	for _, opt := range opts {
		opt(req)
	}

	resp, err := c.api.Close(c.ctx, req)

	if err != nil {
		return nil, err
	}

	return mt5grpc.ParseMT5GRPCResponse[*pb.OrderSendResult, types.OrderSendResult](resp, func() *pb.OrderSendResult {
		return resp.GetOrderSendResult()
	})
}
