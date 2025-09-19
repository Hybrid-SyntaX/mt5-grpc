package client

import (
	"github.com/hybrid-syntax/mt5-grpc/go/mt5grpc"
	"github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/core/enums"
	"github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/core/types"
	pb "github.com/hybrid-syntax/mt5-grpc/go/mt5grpc/generated_proto"
	"google.golang.org/protobuf/types/known/timestamppb"
	"time"
)

func (c *Client) CopyRatesRange(
	symbol string,
	timeframe enums.TimeFrame,
	dateFrom time.Time,
	dateTo time.Time,
) (*types.Rates, error) {

	resp, err := c.api.CopyRatesRange(c.ctx, &pb.CopyRatesRangeRequest{
		Symbol:    symbol,
		Timeframe: pb.TimeFrame(timeframe),
		DateFrom:  timestamppb.New(dateFrom),
		DateTo:    timestamppb.New(dateTo),
	})
	if err != nil {
		return nil, err
	}

	return mt5grpc.ParseMT5GRPCResponse[*pb.Rates, types.Rates](resp,
		func() *pb.Rates {
			return resp.GetRates()
		})
}

func (c *Client) CopyRatesFrom(
	symbol string,
	timeframe enums.TimeFrame,
	dateFrom time.Time,
	count int32,
) (*types.Rates, error) {

	resp, err := c.api.CopyRatesFrom(c.ctx, &pb.CopyRatesFromRequest{
		Symbol:    symbol,
		Timeframe: pb.TimeFrame(timeframe),
		DateFrom:  timestamppb.New(dateFrom),
		Count:     count,
	})
	if err != nil {
		return nil, err
	}

	return mt5grpc.ParseMT5GRPCResponse[*pb.Rates, types.Rates](resp,
		func() *pb.Rates {
			return resp.GetRates()
		})
}

func (c *Client) CopyRatesFromPos(
	symbol string,
	timeframe enums.TimeFrame,
	startPos int64,
	count int32,
) (*types.Rates, error) {

	resp, err := c.api.CopyRatesFromPos(c.ctx, &pb.CopyRatesFromPosRequest{
		Symbol:    symbol,
		Timeframe: pb.TimeFrame(timeframe),
		StartPos:  startPos,
		Count:     count,
	})
	if err != nil {
		return nil, err
	}

	return mt5grpc.ParseMT5GRPCResponse[*pb.Rates, types.Rates](resp,
		func() *pb.Rates {
			return resp.GetRates()
		})
}

func (c *Client) CopyTicksFrom(
	symbol string,
	dateFrom time.Time,
	count int32,
	flags int32,
) (*types.Ticks, error) {
	resp, err := c.api.CopyTicksFrom(c.ctx, &pb.CopyTicksFromRequest{
		Symbol:   symbol,
		DateFrom: timestamppb.New(dateFrom),
		Count:    count,
		Flags:    flags,
	})
	if err != nil {
		return nil, err
	}

	return mt5grpc.ParseMT5GRPCResponse[*pb.Ticks, types.Ticks](resp,
		func() *pb.Ticks {
			return resp.GetTicks()
		})
}

func (c *Client) CopyTicksRange(
	symbol string,
	dateFrom time.Time,
	dateTo time.Time,
	flags int32,
) (*types.Ticks, error) {
	resp, err := c.api.CopyTicksRange(c.ctx, &pb.CopyTicksRangeRequest{
		Symbol:   symbol,
		DateFrom: timestamppb.New(dateFrom),
		DateTo:   timestamppb.New(dateTo),
		Flags:    flags,
	})
	if err != nil {
		return nil, err
	}

	return mt5grpc.ParseMT5GRPCResponse[*pb.Ticks, types.Ticks](resp,
		func() *pb.Ticks {
			return resp.GetTicks()
		})
}
